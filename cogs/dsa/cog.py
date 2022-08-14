import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import testServerID
from typing import Optional
from .dice_dropdown import DiceDropdownView
from .coinflip_buttons import Coinflip

# Initialize Cog
class DSA(commands.Cog, name="DSA"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Dice commands
    @nextcord.slash_command(name="dice", description="Verschiedene Würfel-Optionen", guild_ids=[testServerID])
    async def dice(self, interaction: Interaction):
        pass
    
    @dice.subcommand(name="roll", description="Würfel werfen!")
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)
        
    @dice.subcommand(name="multi", description="Mehrere Würfel werfen!")
    async def dice_multiple(self, interaction: Interaction, dice: Optional[str] = SlashOption(name="")):
        # TODO: Think of a easily extensible dice roll format, parsable by regex
        pass
        
    @dice.subcommand(name="help", description="Mehrere Würfel werfen!")
    async def dice_multiple(self, interaction: Interaction, dice: Optional[str] = SlashOption(name="")):
        # TODO: Explain dice roll format
        pass
     
       
    # Coin-Flip commands
    @nextcord.slash_command(name="coin", description="Verschiedene Münz-Werf-Optionen", guild_ids=[testServerID])
    async def coin(self, interaction: Interaction):
        pass

    @coin.subcommand(name="flip", description="Wirf eine Münze!")
    async def coin_flip(self, interaction: Interaction):
        await interaction.send(view=Coinflip(), ephemeral=True)


    # TODO: Character Templates
    @nextcord.slash_command(name="template", description="Charakter-Templates & mehr!", guild_ids=[testServerID])
    async def template(self, interaction: Interaction):
        pass
        
    @template.subcommand(name="get_template", description="Lade das Charakter-Template als PDF herunter.")
    async def template_download(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @template.subcommand(name="import", description="Importiere einen Charakter per PDF.")
    async def template_import(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @template.subcommand(name="export", description="Exportiere einen Charakter als PDF.")
    async def template_export(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)


    # TODO: Character Editors
    @nextcord.slash_command(name="character", description="Charakter-Optionen!", guild_ids=[testServerID])
    async def character(self, interaction: Interaction):
        pass
           
    @character.subcommand(name="list", description="Zeigt alle gespeicherten Charaktere an.")
    async def chars_list(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @character.subcommand(name="edit", description="Bearbeitet einen gespeicherten Charakter.")
    async def char_edit(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)
    
    @character.subcommand(name="delete", description="Löscht einen ausgewählten Charakter.")
    async def char_del(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)

    @character.subcommand(name="reset", description="Löscht ALLE gespeicherten Charaktere!")
    async def char_del_all(self, interaction: Interaction):
        await interaction.response.send_message("In developement!", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(DSA(bot))
    print("DSA module loaded!")
