import nextcord
import uuid
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
from functions.helpers import EmbedBuilder, is_valid_time_format
from functions.logging import logging
from functions.tasks import set_task, stop_task
from functions.paths import sunny, questioning
from functions.errors import default_error, dm_error, perm_error
from main import db_tasks


# Initialize Cog
class Mood(commands.Cog, name="Mood"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Mood
    @nextcord.slash_command(name="mood", description="How's your mood?")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def main(self, interaction: Interaction) -> None:
        pass
    
    
    @main.subcommand(name="poll", description="Ask the community!")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    @commands.has_permissions(create_public_threads=True)
    async def mood_poll(self, interaction: Interaction,
                        time: str = SlashOption(
                            description="Time in HH:MM format"),
                        role: nextcord.Role = SlashOption(
                            description="Select a role to ping!", required=False, default="None"),
                        thread: bool = SlashOption(
                            description="Automatically create a thread?", required=False, default=False),
                        lang: str = SlashOption(description="Choose your langauge!", required=False, default="en", choices={
                            "English": "en",
                            "Deutsch": "de"
                        })) -> None:
        await interaction.response.defer()

        if is_valid_time_format(time):
            if db_tasks.open.count_documents({"server_id": interaction.guild.id, "type": "mood"}) < 1:
                uuid_id = uuid.uuid4()

                if role == "None":
                    role_id = "None"
                else:
                    role_id = role.id

                task = {
                    "internal_id": f"{uuid_id}",
                    "type": "mood",
                    "server_id": interaction.guild.id,
                    "channel_id": interaction.channel.id,
                    "role_id": role_id,
                    "time": time,
                    "mode": "None",
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

                em = EmbedBuilder.bake_thumbnail(embed)
                await interaction.followup.send(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)

            else:
                if lang == "en":
                    embed = {
                        "title": "There already is a task set!",
                        "description": "Please delete the existing one first, using `/mood remove`, if you want to create a new one!"
                    }
                elif lang == "de":
                    embed = {
                        "title": "Es gibt bereits eine offene Aufgabe!",
                        "description": "Um sie zu bearbeiten, nutze bitte `/mood remove` um den bestehenden Eintrag zu löschen!"
                    }

                em = EmbedBuilder.bake_thumbnail(embed)
                await interaction.followup.send(file=EmbedBuilder.get_emoji(questioning), embed=em, ephemeral=True)

        else:
            raise commands.errors.BadArgument
        
    @mood_poll.error
    async def on_command_error(self, interaction: Interaction, error) -> None:
        if isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await dm_error(interaction)
        if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
            await perm_error(interaction)
        else:
            await default_error(interaction)
            
# Add Cog to bot


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Mood(bot))
    logging.info("Mood module loaded!")
