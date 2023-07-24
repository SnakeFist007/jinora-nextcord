import os
import logging
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from functions.helpers import parse_json, parse_embed, load_error_msg
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

## Variables
load_dotenv()
token = os.getenv("TOKEN")
uri = os.getenv("MONGODB")
url = os.getenv("STABLEDIFFUSION")

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


# * Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
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

## Events
# * ON STARTUP
@bot.event
async def on_ready():
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
    if db_servers.joined_servers_list.find_one( { "server_id": guild.id } ) is None:
        db_servers.joined_servers_list.insert_one( { "server_id": guild.id } )
        logging.info(f"Added server {guild.id} to database.")
    else:
        logging.warning(f"Server {guild.id} was already on the list!")

    # Send welcome message to system channel, if available
    if guild.system_channel is not None:
        em = parse_embed("database/embeds/welcome_embed.json")
        await guild.system_channel.send(embed=em)
    

# * ON SERVER LEAVE
@bot.event
async def on_guild_remove(guild):
    logging.info(f"Left server {guild.id}!")
    # Check if server ID was already deleted from the list
    if db_servers.joined_servers_list.find_one( { "server_id": guild.id } ) is not None:
        db_servers.joined_servers_list.delete_one( { "server_id": guild.id } )
        logging.info(f"Removed server {guild.id} from database.")
    else:
        logging.warning(f"Server {guild.id} was already removed from the list!")


## * Main run function
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
