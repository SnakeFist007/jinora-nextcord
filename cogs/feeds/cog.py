import nextcord
import asyncio
import uuid
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from main import logging
from main import set_reminder, bake_embed, em_error
from main import db_tasks
from main import TIMEZONE


def convert_day(day):
    key = { 0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday" }
    
    return key[day]

# Initialize Cog
class Feeds(commands.Cog, name="Feeds"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    # TODO: Optional event creation, instead of a webhook -> separate command!
    # Command group: /feed ...
    @nextcord.slash_command(name="feed", description="Recurring reminders!")
    async def main(self, interaction: Interaction):
        pass
    
    
    # Add feeds & start reminder countdown
    @main.subcommand(name="add", description="Creates a recurring reminder.")
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
        uuid_id = uuid.uuid4()
        task = {
            "webhook": webhook,
            "internal_id": f"{uuid_id}",
            "server_id": interaction.guild.id,
            "user_id": interaction.user.id,
            "role_id": role.id,
            "day": day,
            "time": time,
            "message": message
        }
        
        embed = {
            "title": "Reminder succesfully created!",
            "description": f"Your reminder `{message}` for <@&{role.id}> was set! Running every {convert_day(day)} at {time}."
        }
              
        db_tasks.open.insert_one(task)
        asyncio.create_task(set_reminder(task, TIMEZONE))
        
        await interaction.response.send_message(embed=bake_embed(embed), ephemeral=True)
        
    
    # Shows all currently active feeds for the user
    @main.subcommand(name="view", description="Lists all active feeds.")
    async def feed_view(self, interaction: Interaction):
        embed = { "title": "Active Feeds" }
        em = bake_embed(embed)
        
        open_tasks = list(db_tasks.open.find({"user_id": interaction.user.id, "server_id": interaction.guild.id}))
        if open_tasks:
            for index, task in enumerate(open_tasks):
                em.add_field(name=f"Task #{index + 1} | {convert_day(task['day'])} - {task['time']}", 
                             value=f"<@&{task['role_id']}> {task['message']}\n**ID:** {task['internal_id']}")
        else:
            em.add_field(name="No feeds found!",
                         value="Add a feed with the `/feed` command.")
            
        await interaction.response.send_message(embed=em, ephemeral=True)
    
    
    # Deletes a feed by its uuid from the user
    @main.subcommand(name="delete", description="Deletes a feed by its ID.")
    async def feed_delete(self, interaction: Interaction, feed_id: str = SlashOption()):
        embed = {
                "title": "Feed deletion successful!",
                "description": f"Deleted feed: {feed_id}"
            }
        em = bake_embed(embed)
        
        try:
            logging.warning(f"Deleting entry {feed_id} from task database!")
            db_tasks.open.delete_one({"internal_id": feed_id})
            await interaction.send(embed=em, ephemeral=True)
        except Exception as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return
    
    
    # Command subgroup: /feed admin ...
    @main.subcommand(name="admin", description="Feed admin tools!")
    async def main_group(self, interaction: nextcord.Interaction):
        pass
    
    
    # Shows all currently active feeds for the server
    @main_group.subcommand(name="view", description="Lists all active feeds from the server.")
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_view(self, interaction: Interaction):
        embed = { 
                 "title": "Active Server-Feeds" 
            }
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
    
    
    # Deletes a feed by its uuid from the server
    @main_group.subcommand(name="delete", description="Deletes a feed from the server.")
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_delete(self, interaction: Interaction, feed_id: str = SlashOption()):
        embed = {
                "title": "Feed deletion successful!",
                "description": f"Deleted feed {feed_id}."
            }
        em = bake_embed(embed)
        
        try:
            logging.warning(f"Deleting entry {feed_id} from task database!")
            db_tasks.open.delete_one({"internal_id": feed_id})
            await interaction.send(embed=em, ephemeral=True)
        except Exception as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return


# Add Cog to bot
def setup(bot):
    bot.add_cog(Feeds(bot))
    logging.info("Feeds module loaded!")
