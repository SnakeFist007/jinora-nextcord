import os
import logging
import nextcord
import asyncio
from nextcord.ext import commands
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from discord_webhook import DiscordWebhook as Webhook
from datetime import datetime, timedelta
from dateutil import tz
from functions.helpers import *

# Variables
load_dotenv()
token = os.getenv("TOKEN")
uri = os.getenv("MONGODB")
url = os.getenv("STABLEDIFFUSION")
timezone = os.getenv("TIMEZONE")

if not token:
    logging.exception(".env - Bot-Token is empty!")
    exit(1)
if not uri:
    logging.exception(".env - MongoDB URI is empty!")
    exit(1)
if not url:
    logging.exception(".env - Stable Diffusion URL is empty!")
    exit(1)

# * MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db_servers = client.servers
db_roles = client.servers.roles
db_reminders = client.reminders
db_tasks = client.tasks

# * Intents & Bot initialization
intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None)

# * Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("jinora-nextcord.log"),
        logging.StreamHandler()
    ]
)


# * Reminders
# Calculate next occurance of weekday
def get_weekday(desired_day, zone):
    next_day = (desired_day - datetime.now(zone).weekday()) % 7
    if next_day == 0:
        next_day = 7
    result = datetime.now(zone) + timedelta(days=next_day)
    
    return result

# Generate reminder & send reminder when ready
async def set_reminder(task, timezone):
    webhook = Webhook(url=task["webhook"], content=f"<@&{task['role_id']}>")
    zone = tz.gettz(timezone)
    dt_time = datetime.strptime(task["time"], "%H:%M")
    
    # Get next occurance
    next_date = get_weekday(task["day"], zone)
    
    # Prepare message
    embed = {
        "title": "Reminder!",
        "description": f"{task['message']}"
    }
    
    webhook.add_embed(bake_raw(embed))
    
    # Start scheduled reminder
    next_reminder = next_date.replace(hour=dt_time.hour, minute=dt_time.minute, second=0)
    wait_time = (next_reminder - datetime.now(zone)).total_seconds()
    logging.info(f"Setting reminder timer for {wait_time} seconds...")
    
    await asyncio.sleep(wait_time)
    
    try:
        webhook.execute()
        logging.info(f"Sending embed through webhook: {task['webhook']}")
    except Exception as e:
        logging.exception(e)


# Events
# * ON STARTUP
@bot.event
async def on_ready():
    # Grab open tasks from MongoDB
    logging.info("Grabbing open tasks from database...")
    open_tasks = db_tasks.open.find({})
    if open_tasks:
        for task in open_tasks:
            logging.info(f"Open task: {task} found!")
            asyncio.create_task(set_reminder(task, timezone))
    else:
        logging.info("No open tasks!")
        
    logging.info("Jinora#2184 is ready!")
    try:
        await bot.sync_application_commands()
        logging.info("Synced global commands!")
    except Exception as e:
        logging.exception(e)
    # Set presence message
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# * ON SERVER JOIN
@bot.event
async def on_guild_join(guild):
    logging.info(f"Joined server {guild.id}!")
    # Check if server ID has already been added to the list
    if db_servers.joined_servers_list.find_one({"server_id": guild.id}) is None:
        db_servers.joined_servers_list.insert_one({"server_id": guild.id})
        logging.info(f"Added server {guild.id} to database.")
    else:
        logging.warning(f"Server {guild.id} was already on the list!")

    # Send welcome message to system channel, if available
    if guild.system_channel is not None:
        await guild.system_channel.send(embed=em_welcome())


# * ON SERVER LEAVE
@bot.event
async def on_guild_remove(guild):
    logging.info(f"Left server {guild.id}!")
    # Check if server ID was already deleted from the list
    if db_servers.joined_servers_list.find_one({"server_id": guild.id}) is not None:
        db_servers.joined_servers_list.delete_one({"server_id": guild.id})
        logging.info(f"Removed server {guild.id} from database.")
    else:
        logging.warning(f"Server {guild.id} was already removed from the list!")


# * Main run function
def main():
    logging.info("Loading modules...")

    # Connect to MongoDB
    try:
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB!")
    except Exception as e:
        logging.exception(e)

    # Load cogs
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")

    # Start the bot
    try:
        bot.run(token)
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
