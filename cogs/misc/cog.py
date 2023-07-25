import nextcord
import requests
import asyncio
from nextcord.interactions import Interaction
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands
from main import logging
from main import db_servers, db_tasks
from main import parse_json, set_reminder
from main import url, timezone


def load_embed():
    defaults = parse_json("database/embeds/status_embed.json")
    return defaults


# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    # General stats of the bot
    @nextcord.slash_command(name="status", description="Pong!")
    async def status(self, interaction: Interaction):
        logging.info("Checking status...")
        # Get amount of servers joined
        count = db_servers.joined_servers_list.count_documents({})
        # Calculate latency
        ping = round(self.bot.latency * 1000)
        logging.info(f"Ping is {ping}ms.")
        # Check if Stable Diffusion is running
        try:
            requests.get(url=f"{url}/internal/ping")
            sd_status = "OK"
            logging.info("Stable Diffusion is online.")
        except Exception as e:
            sd_status = "Offline"
            logging.warning("Stable Diffusion is offline.")

        embed1 = load_embed()
        embed2 = {
            "description": f"Amount of Servers joined: `{count}`\nPing: `{ping}ms`\nStable Diffusion Status: `{sd_status}`"
        }
        em = Embed().from_dict(embed1 | embed2)

        await interaction.send(embed=em, ephemeral=True)


    # TODO: Create Autofeed view command
    @nextcord.slash_command(name="view", description="Lists all active feeds")
    async def autofeed_view(self, interaction: Interaction):
        open_tasks = db_tasks.open.find({})
        if open_tasks is not None:
            for task in open_tasks:
                logging.info(f"Open task: {task} found!")
                #set_reminder(task)
        else:
            logging.info("No open tasks!")
            
            
    # TODO: Create Autofeed delete command
    @nextcord.slash_command(name="delete", description="Deletes a feed")
    async def autofeed_delete(self, interaction: Interaction, feed: str = SlashOption()):
        # db_tasks.open.delete_one({"_id": task["_id"]})
        pass
    
    
    @nextcord.slash_command(name="autofeed", description="Creates a recurring reminder")
    async def autofeed_create(self, interaction: Interaction,  
                       role: nextcord.Role = SlashOption(), 
                       day: int = SlashOption(
                           choices={
                               "Monday": 0,
                               "Tuesday": 1,
                               "Wednesday": 2,
                               "Thursday": 3,
                               "Friday": 4,
                               "Saturday": 5,
                               "Sunday": 6 
                               }),
                       time: str = SlashOption(),
                       message: str = SlashOption(),
                       webhook: str = SlashOption()):
        
        task = {
            "webhook": webhook,
            "server_id": interaction.guild.id,
            "role_id": role.id,
            "day": day,
            "time": time,
            "message": message
        }
        
        embed1 = parse_json("database/embeds/standard_embed.json")
        embed2 = {
            "title": "Reminder succesfully created!",
            "description": f"Your reminder `{message}` for @{role.name} was set!"
        }
        em = Embed().from_dict(embed1 | embed2)
              
        db_tasks.open.insert_one(task)
        asyncio.create_task(set_reminder(task, timezone))
        
        await interaction.response.send_message(embed=em, ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
