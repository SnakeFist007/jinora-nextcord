import os
import shutil
import logging
import aiosqlite
import nextcord
from nextcord.ext import commands

## Variables
token_file = open("token.auth", "r")
db_servers = "database\servers.db"
db_characters = "database\characters.db"
token = token_file.read()

# Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, help_command=None)

# Logging
logger = logging.getLogger("nextcord")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename="lene-nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


## Events
# ON STARTUP: Set activity and report online state when ready 
@bot.event
async def on_ready():
    print("\n\tLene#2184 is ready!")
    if not os.path.exists(db_servers):
        open(db_servers, "x").close()
        
    if not os.path.exists(db_characters):
        open(db_characters, "x").close()
    
    async with aiosqlite.connect(db_servers) as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS servers (guild INTEGER)")
        await db.commit()
        
    async with aiosqlite.connect(db_characters) as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS characters (user INTEGER, char_name TEXT, location TEXT)")
        await db.commit()
    
    try:
        await bot.sync_application_commands()
        print("\tSynced global commands!")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# ON SERVER JOIN: Send greeting message & create server directory
@bot.event
async def on_guild_join(guild):
    print(f"Joined server {guild.id}!")
    
    # Create DB entry
    async with aiosqlite.connect(db_servers) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"INSERT INTO servers (guild) VALUES ({guild.id})")
        await db.commit()
    
    # Create server sub-directory
    try:
        os.mkdir(f"database\id_store\{guild.id}")
    except FileExistsError:
        print(f"Folder for {guild.id} already exists, cleaning up & creating a fresh directory...")
        shutil.rmtree(f"database\id_store\{guild.id}")
        os.mkdir(f"database\id_store\{guild.id}")
    
    # Send welcome message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Vielen Dank für die Einladung! <3\nBenutze **/help** um mehr über meine Befehle zu lernen!")
        break


# ON SERVER LEAVE:  Clean up server directory
@bot.event
async def on_guild_remove(guild):
    print(f"Left server {guild.id}!")
    
    # Delete server sub-directory
    try:
        shutil.rmtree(f"database\id_store\{guild.id}")
    except FileNotFoundError:
        print(f"PLEASE CHECK: Couldn't find the path specified! (database\id_store\{guild.id})")
        print(f"DATABASE ENTRY NOT REMOVED! MANUAL REMOVAL MIGHT BE NECESSARY: GUILD ID {guild.id}")
    
    # Delete DB entry
    async with aiosqlite.connect(db_servers) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f"DELETE FROM servers WHERE guild={guild.id}")
        await db.commit()



## Main run function
def main():
    # Load extensions
    print("Loading modules... \n")
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    bot.run(token)

if __name__ == "__main__":
    main()
