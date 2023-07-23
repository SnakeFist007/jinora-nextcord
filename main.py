import os
import logging
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from functions.helpers import parse_embed
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

## Variables
load_dotenv()
uri = os.getenv("MONGODB")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.servers

# * Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, help_command=None)

# * Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s : %(asctime)s - %(message)s", 
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
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# * ON SERVER JOIN
@bot.event
async def on_guild_join(guild):
    logging.info(f"Joined server {guild.id}!")
    db.joined_servers_list.insert_one( { "server_id": guild.id } )

    # Send welcome message to system channel, if available
    if guild.system_channel is not None:
        em = parse_embed("database/embeds/welcome_embed.json")
        await guild.system_channel.send(embed=em)


# * ON SERVER LEAVE
@bot.event
async def on_guild_remove(guild):
    logging.info(f"Left server {guild.id}!")
    db.joined_servers_list.delete_one( { "server_id": guild.id } )


## * Main run function
def main():
    # Load extensions
    logging.info("Loading modules... \n")
    
    # Connect to MongoDB   
    try:
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB!")
    except Exception as e:
        logging.exception(e)

    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    try:
        bot.run(os.getenv("TOKEN"))
    except Exception as e:
        logging.exception(e)

if __name__ == "__main__":
    main()
