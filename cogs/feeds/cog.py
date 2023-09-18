import nextcord
import asyncio
import uuid
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from functions.errors import default_error, dm_error, perm_error
from functions.helpers import EmbedBuilder, convert_day, is_valid_time_format, is_valid_webhook
from functions.logging import logging
from functions.reminders import set_reminder
from functions.paths import sunny
from main import db_tasks, TIMEZONE


# Initialize Cog
class Feeds(commands.Cog, name="Feeds"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    
    # Command group: /feed ...
    @nextcord.slash_command(name="feed", description="Recurring reminders!")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def main(self, interaction: Interaction) -> None:
        pass
    
    
    # Add feeds & start reminder countdown
    @main.subcommand(name="add", description="Creates a recurring reminder.")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def feed_add(self, 
                       interaction: Interaction,  
                       role: nextcord.Role = SlashOption(description="Select a role to ping"), 
                       day: int = SlashOption(description="The day of the reminder",
                           choices={
                               "Monday": 0,
                               "Tuesday": 1,
                               "Wednesday": 2,
                               "Thursday": 3,
                               "Friday": 4,
                               "Saturday": 5,
                               "Sunday": 6 
                               }),
                       time: str = SlashOption(description="Time in 24h 'HH:MM' format"),
                       message: str = SlashOption(description="Message of the reminder"),
                       webhook: str = SlashOption(description="Discord webhook URL")) -> None:
        # Check if time was entered correctly
        if is_valid_time_format(time):
            # Check if webhook is valid
            if is_valid_webhook(webhook, interaction.guild.id):
                # Check if limit (5 entries per server) is reached
                if db_tasks.open.count_documents({"server_id": interaction.guild.id}) < 5:
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
                        "description": f"Your reminder `{message}` for <@&{role.id}> was set! Running every {convert_day(day)} at {time}.\n**ID: {uuid_id}**"
                    }
                    
                    db_tasks.open.insert_one(task)
                    asyncio.create_task(set_reminder(task, TIMEZONE))
                    
                else:
                    embed = {
                        "title": "Server limit reached!",
                        "description": "You already have 5 tasks registered, you can't add any more!"
                    }
            else:
                embed = {
                    "title": "Invalid Webhook!",
                    "description": "Please enter a correct webhook url."
                }
        else:
            embed = {
                "title": "Wrong time format!",
                "description": "Please input the time as 'HH:MM' and in 24h format!"
            }
        
        await interaction.response.send_message(file=EmbedBuilder.get_emoji(sunny), embed=EmbedBuilder.bake(embed), ephemeral=True)
        
    
    # Shows all currently active feeds for the user
    @main.subcommand(name="view", description="Lists all active feeds.")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def feed_view(self, interaction: Interaction) -> None:
        embed = { "title": "Active Feeds" }
        em = EmbedBuilder.bake(embed)
        
        open_tasks = list(db_tasks.open.find({"user_id": interaction.user.id, "server_id": interaction.guild.id}))
        if open_tasks:
            for index, task in enumerate(open_tasks):
                em.add_field(
                    name=f"Task #{index + 1} | {convert_day(task['day'])} - {task['time']}", 
                    value=f"<@&{task['role_id']}> {task['message']}\n**ID:** {task['internal_id']}",
                    inline=False
                )
        else:
            em.add_field(
                name="No feeds found!",
                value="Add a feed with the `/feed` command."
            )
            
        await interaction.response.send_message(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)
    
    
    # Deletes a feed by its uuid from the user
    @main.subcommand(name="delete", description="Deletes a feed by its ID.")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def feed_delete(self, interaction: Interaction, feed_id: str = SlashOption()) -> None:
        embed = {
                "title": "Feed deletion successful!",
                "description": f"Deleted feed: {feed_id}"
            }
        em = EmbedBuilder.bake(embed)
        
        if db_tasks.open.find_one({"user_id": interaction.user.id, "internal_id": feed_id}):
            try:
                logging.warning(f"Deleting entry {feed_id} from task database!")
                db_tasks.open.delete_one({"internal_id": feed_id})
                await interaction.send(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)
            except Exception as e:
                logging.exception(e)
                raise commands.errors.BadArgument
        else:
            raise commands.errors.BadArgument
    
    
    # Command subgroup: /feed admin ...
    @main.subcommand(name="admin", description="Feed admin tools!")
    @application_checks.guild_only()
    @application_checks.has_permissions(administrator=True)
    async def main_group(self, interaction: Interaction) -> None:
        pass
    
    
    # Shows all currently active feeds for the server
    @main_group.subcommand(name="view", description="Lists all active feeds from the server.")
    @application_checks.guild_only()
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_view(self, interaction: Interaction) -> None:
        embed = { 
                 "title": "Active Server-Feeds" 
            }
        em = EmbedBuilder.bake(embed)
        
        open_tasks = list(db_tasks.open.find({"server_id": interaction.guild.id}))
        if open_tasks:
            for index, task in enumerate(open_tasks):
                em.add_field(name=f"Task #{index + 1} | {convert_day(task['day'])} - {task['time']}", 
                             value=f"<@&{task['role_id']}> {task['message']}\n**ID:** {task['internal_id']}")
        else:
            em.add_field(name="No feeds found!",
                         value="Add a feed with the `/feed` command.")
            
        await interaction.response.send_message(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)
    
    
    # Deletes a feed by its uuid from the server
    @main_group.subcommand(name="delete", description="Deletes a feed from the server.")
    @application_checks.guild_only()
    @application_checks.has_permissions(administrator=True)
    async def feed_admin_delete(self, interaction: Interaction, feed_id: str = SlashOption()) -> None:
        embed = {
                "title": "Feed deletion successful!",
                "description": f"Deleted feed {feed_id}."
            }
        em = EmbedBuilder.bake(embed)
        
        try:
            logging.warning(f"Deleting entry {feed_id} from task database!")
            db_tasks.open.delete_one({"internal_id": feed_id})
            await interaction.send(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)
        except Exception as e:
            logging.exception(e)
            return
    
    
    # ERROR HANDLING
    @feed_add.error
    @feed_view.error
    @feed_admin_view.error
    @feed_delete.error
    @feed_admin_delete.error
    async def feed_view_error(self, interaction: Interaction, error) -> None:
        if isinstance(error, commands.errors.BadArgument):
            await default_error(interaction)
        if isinstance(error, application_checks.errors.ApplicationBotMissingPermissions):
            await perm_error(interaction)
        if isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await dm_error(interaction)
        else:
            await default_error(interaction)



# Add Cog to bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Feeds(bot))
    logging.info("Feeds module loaded!")
