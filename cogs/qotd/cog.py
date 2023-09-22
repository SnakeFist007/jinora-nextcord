import nextcord
import uuid
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from functions.apis import get_quote, get_question
from functions.errors import default_error, dm_error, perm_error
from functions.helpers import EmbedBuilder, is_valid_time_format
from functions.logging import logging
from functions.tasks import set_task, stop_task
from functions.paths import reading, sunny, questioning
from main import db_tasks


# Initialize Cog
class QotD(commands.Cog, name="QotD"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # Questions
    @nextcord.slash_command(name="question", description="Question of the day!")
    @application_checks.guild_only()
    async def question(self, interaction: Interaction,
                       lang: str = SlashOption(description="Choose your langauge!", required=False, default="en", choices={
                           "English": "en",
                           "Deutsch": "de"
                       })) -> None:
        output = get_question(lang)
        embed = {
            "title": f"{output}",
            "description": "Need something to reflect on? I've got you covered!\nCome back tomorrow for a new quote."
        }

        await interaction.response.send_message(embed=EmbedBuilder.bake(embed))
    
    
    # Quotes
    @nextcord.slash_command(name="quote", description="Quote of the day!")
    @application_checks.guild_only()
    async def quote(self, interaction: Interaction,
                    lang: str = SlashOption(description="Choose your langauge!", required=False, default="en", choices={
                        "English": "en",
                        "Deutsch": "de"
                    })) -> None:
        try: 
            data = await get_quote(lang)
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*",
                "description": "Sometimes quotes can be very insightful... Other times, not so much."
            }
        
            await interaction.response.send_message(embed=EmbedBuilder.bake(embed))
            
        except ValueError:
            logging.exception("ERROR getting response from quotes API")
            raise commands.errors.BadArgument
    
    
    # Dailies
    @nextcord.slash_command(name="qotd", description="Enables Q of the day!")
    async def main(self, interaction: Interaction) -> None:
        pass
    
    
    # Dailies
    @main.subcommand(name="add", description="Q of the day!")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def qotd_add(self, interaction: Interaction,
                   mode: str = SlashOption(description="Quotes or Questions?",
                                           choices={
                                               "quote": "quote",
                                               "question": "question"
                                           }),
                   time: str = SlashOption(description="Time in HH:MM format"),
                   role: nextcord.Role = SlashOption(description="Select a role to ping!", required=False, default="None"),
                   thread: bool = SlashOption(description="Automatically create a thread?", required=False, default=False),
                       lang: str = SlashOption(description="Choose your langauge!", required=False, default="en", choices={
                       "English": "en",
                       "Deutsch": "de"
                   })
                   ) -> None:
        
        await interaction.response.defer()
        
        if is_valid_time_format(time):
            if db_tasks.open.count_documents({"server_id": interaction.guild.id, "mode": mode}) < 1:
                uuid_id = uuid.uuid4()
                
                if role == "None":
                    role_id = "None"
                else:
                    role_id = role.id
                
                task = {
                    "internal_id": f"{uuid_id}",
                    "type": "qotd",
                    "server_id": interaction.guild.id,
                    "channel_id": interaction.channel.id,
                    "role_id": role_id,
                    "time": time,
                    "mode": mode,
                    "threading": thread,
                    "lang": lang
                }
                if lang == "en":
                    embed = {
                        "title": "Task succesfully created!"
                    }
                elif lang == "de":
                    embed = {
                        "title": "Aufgabe erfolgreich erstellt!",
                    }

                db_tasks.open.insert_one(task)
                try:
                    asyncio.create_task(set_task(task), name=uuid_id)
                
                except Exception as e:
                    logging.exception(e)
                    raise commands.errors.BadArgument

                em = EmbedBuilder.bake(embed)
                await interaction.followup.send(embed=em, ephemeral=True)
            
            else:
                if lang == "en":
                    embed = {
                        "title": "There already is a task set!",
                        "description": "Please delete the existing one first, using `/qotd remove`, if you want to create a new one!"
                    }
                elif lang == "de":
                    embed = {
                        "title": "Es gibt bereits eine offene Aufgabe!",
                        "description": "Um sie zu bearbeiten, nutze bitte `/qotd remove` um den bestehenden Eintrag zu löschen!"
                    }

                em = EmbedBuilder.bake(embed)
                await interaction.followup.send(embed=em, ephemeral=True)

        else:
            raise commands.errors.BadArgument
        
        
    # Dailies
    @main.subcommand(name="remove", description="Disables Q of the day!")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def qotd_remove(self, interaction: Interaction, mode: str = SlashOption(description="The mode to remove",
                                                                                  choices={
                                                                                      "quote": "quote",
                                                                                      "question": "question"
                                                                                  })) -> None:
    
        try:
            task = db_tasks.open.find_one(
                {"server_id": interaction.guild.id, "mode": mode})
            
            if task:
                logging.warning(f"Deleting entry {task['internal_id']} from task database!")
                db_tasks.open.delete_one({"internal_id": task['internal_id']})
                await stop_task(task['internal_id'])
                
                embed = { "title": "Q of the Day",
                         "description": f"Removed daily {mode}!" }

            else:
                embed = { "title": "Q of the Day",
                         "description": f"No active daily {mode} found!" }
                
            em = EmbedBuilder.bake(embed)
            await interaction.response.send_message(embed=em, ephemeral=True)
        
        except Exception:
            raise commands.errors.BadArgument
    


    @quote.error
    @question.error
    @qotd_add.error
    @qotd_remove.error
    async def on_command_error(self, interaction: Interaction, error) -> None:
        if isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await dm_error(interaction)
        if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
            await perm_error(interaction)
        else:
            await default_error(interaction)
        

# Add Cog to bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(QotD(bot))
    logging.info("QotD module loaded!")
