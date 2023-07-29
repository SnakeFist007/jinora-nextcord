import os
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
from functions.logging import logging
from functions.nextcordConsole.console import Console
from functions.paths import *


# Setup
VERSION="1.1.0"

# * Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
URI = os.getenv("MONGODB")
WEATHER = os.getenv("WEATHER")
QUOTES = os.getenv("QUOTES")
TIMEZONE = os.getenv("TIMEZONE")

# Check if .env is filled out correctly
def check_dotenv(var, error):
    if not var:
        logging.critical(f".env - {error} is empty!")
        exit(1)
        
check_dotenv(TOKEN, "Bot-Token")
check_dotenv(URI, "MongoDB URI")
check_dotenv(WEATHER, "Weather API")
check_dotenv(QUOTES, "Quotes API")
check_dotenv(TIMEZONE, "Timezone")

# * MongoDB
client = MongoClient(URI, server_api=ServerApi('1'))
db_servers = client.servers
db_tasks = client.tasks

# * Intents & Bot initialization
intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None, owner_id=83931378097356800)
console = Console(bot)



# Functions
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
    # Prepare message
    webhook = Webhook(url=task["webhook"], content=f"<@&{task['role_id']}>")
    embed = {
        "title": "Reminder!",
        "description": f"{task['message']}"
    }
    webhook.add_embed(bake_raw(embed))
    
    # Get next occurance
    zone = tz.gettz(timezone)
    dt_time = datetime.strptime(task["time"], "%H:%M")
    next_date = get_weekday(task["day"], zone)
    
    # Start scheduled reminder
    next_reminder = next_date.replace(hour=dt_time.hour, minute=dt_time.minute, second=0)
    wait_time = (next_reminder - datetime.now(zone)).total_seconds()
    logging.info(f"Setting reminder timer for {wait_time} seconds...")
    
    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)
    try:
        webhook.execute()
        logging.info(f"Reminder triggered: Sending embed through webhook: {task['webhook']}")
        # Set new reminder
        set_reminder(task, timezone)
    except Exception as e:
        logging.exception(e)
        return



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
            asyncio.create_task(set_reminder(task, TIMEZONE))
    else:
        logging.info("No open tasks!")
    
    # Send ready message, sync commands    
    logging.info("Jinora#2184 is ready!")
    try:
        await bot.sync_application_commands()
        logging.info("Synced global commands!")
    except Exception as e:
        logging.exception(e)
        return
        
    # Set presence message
    logging.info("Setting presence message...")
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



# * CONSOLE COMMANDS
# Console help
@console.command()
async def help():
    print("$ Following commands are available: help, reload")
    
# Hot-reload all cogs
@console.command()
async def reload():
    print("$ Hot-reloading all cogs!")
    logging.warning("Reloading all cogs!")
    for folder in cogs.iterdir():
        if (folder / "cog.py").exists():
            bot.reload_extension(f"cogs.{folder.name}.cog")



# * Main run function
def main():
    # Connect to MongoDB
    try:
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB!")
    except Exception as e:
        logging.exception(e)
        return

    # Load cogs
    logging.info("Loading modules...")
    for folder in cogs.iterdir():
        if (folder / "cog.py").exists():
            bot.load_extension(f"cogs.{folder.name}.cog")

    # Start the bot
    try:
        logging.info("Starting bot...")
        console.start()
        bot.run(TOKEN)
    except Exception as e:
        logging.exception(e)
        return


if __name__ == "__main__":
    main()
