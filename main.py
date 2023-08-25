#
# ────▓▓▓▓▓▓──────
# ───▓▄▓▓▓▓▓▓─────
# ──────▓▓▓▓▓─▓───
# ─▓▓▓▓▓▓▓▓▓──▓▓──
# ▓▓▓▓▓──────▓▓▓▓─
# ─▓▓▓▓▓───▓▓▓▓▓──
# ──▓▓▓▓▓▓▓▓▓▓▓───
# ─────▓▓▓▓▓──────
#
# Made by: https://github.com/SnakeFist007 - 2023
#

import pretty_errors
import os
import nextcord
import asyncio
from nextcord.ext import commands
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi as ServerAPI
from functions.nextcordConsole.console import Console
from functions.helpers import EmbedHandler
from functions.logging import logging
from functions.paths import cogs, ascii_art
from functions.reminders import set_reminder


# Setup
# * Load .env
load_dotenv()
VERSION = "1.4.1"
OWNER_ID = 83931378097356800
FEEDBACK_ID = 1140961474718744636
TOKEN = os.getenv("TOKEN")
PAPERTRAIL_URL = os.getenv("PAPERTRAIL_URL")
PAPERTRAIL_PORT = int(os.getenv("PAPERTRAIL_PORT"))
URI = os.getenv("MONGODB")
WEATHER = os.getenv("WEATHER")
QUOTES = os.getenv("QUOTES")
TIMEZONE = os.getenv("TIMEZONE")

# Check if .env is filled out correctly
def check_dotenv(var, error: str) -> None:
    if not var:
        logging.critical(f".env - {error} is empty!")
        exit()
        
check_dotenv(TOKEN, "Bot-Token")
check_dotenv(PAPERTRAIL_URL, "Papertrail URL")
check_dotenv(PAPERTRAIL_PORT, "Papertrail Port")
check_dotenv(URI, "MongoDB URI")
check_dotenv(WEATHER, "Weather API")
check_dotenv(QUOTES, "Quotes API")
check_dotenv(TIMEZONE, "Timezone")

# * MongoDB
client = MongoClient(URI, server_api=ServerAPI("1"))
db_servers = client.servers
db_tasks = client.tasks

# * Intents & Bot initialization
intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None, owner_id=OWNER_ID)
console = Console(bot)



# Events
# * ON STARTUP
@bot.event
async def on_ready() -> None:
    # Grab open tasks from MongoDB
    logging.info("Grabbing open tasks from database...")
    open_tasks = db_tasks.open.find({})
    if open_tasks:
        for task in open_tasks:
            logging.info(f"Open task: {task['internal_id']} found!")
            asyncio.create_task(set_reminder(task, TIMEZONE))
    else:
        logging.info("No open tasks!")
    
    # Send ready message, sync commands    
    logging.info(f"Jinora#2184 (v{VERSION}) is ready!")
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
async def on_guild_join(guild) -> None:
    logging.info(f"Joined server {guild.id}!")
    
    # Check if server ID has already been added to the list
    if db_servers.joined_servers_list.find_one({"server_id": guild.id}) is None:
        db_servers.joined_servers_list.insert_one({"server_id": guild.id})
        logging.info(f"Added server {guild.id} to database.")
    else:
        logging.warning(f"Server {guild.id} was already on the list!")

    # Send welcome message to system channel, if available
    if guild.system_channel is not None:
        await guild.system_channel.send(embed=EmbedHandler.welcome())


# * ON SERVER LEAVE
@bot.event
async def on_guild_remove(guild) -> None:
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
async def help() -> None:
    print("$ Following commands are available: help, reload, load, unload")
    
    
# Cog Mangement
# Hot-reload all cogs
@console.command()
async def reload() -> None:
    print("$ Hot-reloading all cogs!")
    logging.warning("Reloading all cogs!")
    for folder in cogs.iterdir():
        if (folder / "cog.py").exists():
            bot.reload_extension(f"cogs.{folder.name}.cog")
            
    await bot.sync_application_commands()
            
# Load a specific cog
@console.command()
async def load(cog: str) -> None:
    try:
        print(f"$ Loading cog {cog}...")
        logging.warning(f"Loading cog {cog}...")
        bot.load_extension(f"cogs.{cog}.cog")
        await bot.sync_application_commands()
    except ModuleNotFoundError:
        logging.error(f"No module named {cog}!")
      
# Unload a specifc cog
@console.command()
async def unload(cog: str) -> None:
    try:
        print(f"$ Unloading cog {cog}...")
        logging.warning(f"Unloading cog {cog}...")
        bot.unload_extension(f"cogs.{cog}.cog")
        logging.info("Unload successful!")
        await bot.sync_application_commands()
    except ModuleNotFoundError:
        logging.error(f"No module named {cog}!")
        
@console.command()
async def leave(id: int) -> None:
    try:
        print(f"$ Leaving server {id}...")
        logging.warning(f"Leaving server {id}...")
        await bot.get_guild(id).leave()
        logging.info("Left server!")
    except AttributeError:
        logging.error(f"No server with ID {id} found!")
            
            
            
# * Main run function
def main() -> None:
    # Print ASCII art
    print(open(ascii_art, "r").read())
    # Connect to MongoDB
    try:
        client.admin.command("ping")
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
