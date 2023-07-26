import nextcord
import asyncio
from nextcord.interactions import Interaction
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands, application_checks
from typing import Optional
from main import logging
from main import db_servers, db_tasks
from main import parse_json, set_reminder, bake_embed
from main import url, timezone


def load_embed():
    defaults = parse_json("database/embeds/status_embed.json")
    return defaults

def convert_day(day):
    key = { 0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday" }
    
    return key[day]


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

        embed = {
            "description": f"Amount of Servers joined: `{count}`\nPing: `{ping}ms`"
        }

        await interaction.send(embed=bake_embed(embed), ephemeral=True)
    
    
    @nextcord.slash_command(name="feed", description="Create recurring reminders for the server")
    async def main(self, interaction: Interaction):
        pass
    
    @main.subcommand(name="add", description="Creates a reminder")
    async def feed_add(self, interaction: Interaction,  
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
            "user_id": interaction.user.id,
            "role_id": role.id,
            "day": day,
            "time": time,
            "message": message
        }
        
        embed = {
            "title": "Reminder succesfully created!",
            "description": f"Your reminder `{message}` for <&@{role.id}> was set! Running every {convert_day(day)} at {time}."
        }
              
        db_tasks.open.insert_one(task)
        asyncio.create_task(set_reminder(task, timezone))
        
        await interaction.response.send_message(embed=bake_embed(embed), ephemeral=True)
        
    
    @main.subcommand(name="view", description="Lists all active feeds")
    async def feed_view(self, interaction: Interaction):
        embed = { "title": "Active Feeds" }
        em = bake_embed(embed)
        
        open_tasks = list(db_tasks.open.find({"user_id": interaction.user.id, "server_id": interaction.guild.id}))
        if open_tasks:
            for index, task in enumerate(open_tasks):
                em.add_field(name=f"Task #{index + 1} | {convert_day(task['day'])} - {task['time']}", 
                             value=f"<&@{task['role_id']}> {task['message']}")
        else:
            em.add_field(name="No feeds found!",
                         value="Add a feed with the `/feed` command.")
            
        await interaction.response.send_message(embed=em, ephemeral=True)
    
        
    # TODO: Create Autofeed delete command
    @main.subcommand(name="delete", description="Deletes a feed")
    async def feed_delete(self, interaction: Interaction, feed: Optional[str] = SlashOption(), 
                              purge: Optional[str] = SlashOption(
                                    choices={"True": "True",
                                             "False": "False"}
                                    )):
        # db_tasks.open.delete_one({"_id": task["_id"]})
        pass
    
    
    @main.subcommand(name="admin", description="Admin commands")
    async def main_group(self, interaction: nextcord.Interaction):
        pass
    
    
    @main_group.subcommand(name="view", description="Lists all active feeds from the server")
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_view(self, interaction: Interaction):
        embed = { "title": "Active Feeds" }
        em = bake_embed(embed)
        
        open_tasks = list(db_tasks.open.find({"server_id": interaction.guild.id}))
        if open_tasks:
            for index, task in enumerate(open_tasks):
                em.add_field(name=f"Task #{index + 1} | {convert_day(task['day'])} - {task['time']}", 
                             value=f"<&@{task['role_id']}> {task['message']}")
        else:
            em.add_field(name="No feeds found!",
                         value="Add a feed with the `/feed` command.")
            
        await interaction.response.send_message(embed=em, ephemeral=True)
    
    
    # TODO: Create Autofeed admin delete command (delete a feed from server)
    @main_group.subcommand(name="delete", description="Deletes a feed from the server")
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_delete(self, interaction: Interaction, feed: Optional[str] = SlashOption(), 
                              purge: Optional[str] = SlashOption(
                                    choices={"True": "True",
                                             "False": "False"}
                                    )):
        # db_tasks.open.delete_one({"_id": task["_id"]})
        pass


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
