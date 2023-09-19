import nextcord
import uuid
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from functions.apis import get_quote, get_question
from functions.errors import default_error, dm_error, perm_error
from functions.helpers import EmbedBuilder, is_valid_time_format
from functions.logging import logging
from functions.tasks import set_daily
from functions.paths import reading, sunny
from main import db_daily


# Initialize Cog
class QotD(commands.Cog, name="QotD"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # Questions
    @nextcord.slash_command(name="question", description="Question of the day!")
    @application_checks.guild_only()
    async def question(self, interaction: Interaction) -> None:
        output = get_question()
        embed = {
            "title": f"{output}",
            "description": "Need something to reflect on? I've got you covered!\nCome back tomorrow for a new quote."
        }

        await interaction.response.send_message(file=EmbedBuilder.get_emoji(reading), embed=EmbedBuilder.bake_thumbnail(embed))
    
    
    # Quotes
    @nextcord.slash_command(name="quote", description="Quote of the day!")
    @application_checks.guild_only()
    async def quote(self, interaction: Interaction) -> None:
        try: 
            data = await get_quote()
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*",
                "description": "Sometimes quotes can be very insightful... Other times, not so much."
            }
        
            await interaction.response.send_message(file=EmbedBuilder.get_emoji(reading), embed=EmbedBuilder.bake_thumbnail(embed))
            
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
                   thread: bool = SlashOption(description="Automatically create a thread?", required=False, default=False)
                   ) -> None:
        
        await interaction.response.defer()
        
        if is_valid_time_format(time):
            uuid_id = uuid.uuid4()
            
            if role == "None":
                role_id = "None"
            else:
                role_id = role.id
            
            daily = {
                "internal_id": f"{uuid_id}",
                "server_id": interaction.guild.id,
                "channel_id": interaction.channel.id,
                "role_id": role_id,
                "time": time,
                "mode": mode,
                "threading": thread
            }
            embed = {
                "title": "Daily succesfully created!",
                "description": f"Sending a daily {mode} every day from now on.\n**ID: {uuid_id}**"
            }

            db_daily.open.insert_one(daily)
            asyncio.create_task(set_daily(daily))

            em = EmbedBuilder.bake_thumbnail(embed)
            await interaction.followup.send(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)

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
        embed = { "title": "Q of the day - Status" }
    
        try:
            daily = db_daily.open.find_one({"server_id": interaction.guild.id, "mode": mode})
            
            if daily:
                logging.warning(f"Deleting entry {daily['internal_id']} from task database!")
                db_daily.open.delete_one({"internal_id": daily['internal_id']})
                
                embed = { "title": "Q of the Day",
                         "description": f"Removed daily {mode}!" }

            else:
                embed = { "title": "Q of the Day",
                         "description": f"No active daily {mode} found!" }
                
            em = EmbedBuilder.bake(embed)
            await interaction.response.send_message(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)
        
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
