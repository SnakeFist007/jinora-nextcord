import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from typing import Optional
from main import testServerID
from .dice_dropdown import DiceDropdownView
from .coinflip_buttons import Coinflip

# Initialize Cog
class DSA(commands.Cog, name="DSA"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Dice & Coins
    @nextcord.slash_command(name="dice_roll", description="Würfel werfen!", guild_ids=[testServerID])
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="coin_flip", description="Wirf eine Münze!", guild_ids=[testServerID])
    async def coin_flip(self, interaction: Interaction):
        await interaction.send(view=Coinflip(), ephemeral=True)


    # Character Templates
    @nextcord.slash_command(name="get_template", description="Lade das Charakter-Template als PDF herunter.", guild_ids=[testServerID])
    async def download_template(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @nextcord.slash_command(name="import", description="Importiere einen Charakter per PDF.", guild_ids=[testServerID])
    async def import_template(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @nextcord.slash_command(name="export", description="Exportiere einen Charakter als PDF.", guild_ids=[testServerID])
    async def export_template(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)


    # Character Editors
    @nextcord.slash_command(name="list_chars", description="Zeigt alle gespeicherten Charaktere an.", guild_ids=[testServerID])
    async def show_chars(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @nextcord.slash_command(name="edit_char", description="Bearbeitet einen gespeicherten Charakter.", guild_ids=[testServerID])
    async def edit_char(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)
    
    @nextcord.slash_command(name="del_char", description="Löscht einen ausgewählten Charakter.", guild_ids=[testServerID])
    async def delete_char(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @nextcord.slash_command(name="reset_chars", description="Löscht ALLE gespeicherten Charaktere!", guild_ids=[testServerID])
    async def delete_all_chars(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(DSA(bot))
    print("DSA module loaded!")
