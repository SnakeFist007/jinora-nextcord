from genericpath import isfile
import nextcord
import os
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import testServerID
from typing import Optional
from .dice_dropdown import DiceDropdownView
from .coinflip_buttons import Coinflip
from .character_dropdown import DelCharDropdownView, DownloadCharDropdownView

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


    # Character Editors
    @nextcord.slash_command(name="character", description="Charakter-Optionen!", guild_ids=[testServerID])
    async def character(self, interaction: Interaction):
        pass
    
    @character.subcommand(name="add", description="Fügt einen mit Optolith erstellten Charakter hinzu.")
    async def char_add_info(self, interaction: Interaction, message):
        await interaction.response.send_message("Bitte nutze das Kontextmenü zum hinzufügen von Charakteren!", ephemeral=True)
     
    @character.subcommand(name="list", description="Zeigt alle gespeicherten Charaktere an.")
    async def chars_list(self, interaction: Interaction):
        # TODO: Show saved characters in an embed
        pass
        
    @character.subcommand(name="download", description="Gibt den gewünschten Charakter als JSON-Datei aus.")
    async def chars_download(self, interaction: Interaction):
        await interaction.send(view=DownloadCharDropdownView(), ephemeral=True)
    
    @character.subcommand(name="delete", description="Löscht einen ausgewählten Charakter.")
    async def char_del(self, interaction: Interaction):
        await interaction.send(view=DelCharDropdownView(), ephemeral=True)

    @character.subcommand(name="reset", description="Löscht ALLE gespeicherten Charaktere!")
    async def char_del_all(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"
        
        if os.path.exists(path):
            for file in os.listdir(path):
                filename = path + file
                if os.path.isfile(filename):
                    os.remove(file)
            os.rmdir(path)
            await interaction.response.send_message("Alle gespeicherten Charaktere gelöscht!", ephemeral=True)      
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
        

    @nextcord.message_command(name="Charakter speichern (JSON)")
    async def char_add(self, interaction: Interaction, message):
        user_id = interaction.user.id
        
        if not str(message.attachments) == "[]":
            # Get the filename
            split_msg = str(message.attachments).split("filename='")[1]
            filename = str(split_msg).split("' ")[0]
            
            if filename.endswith(".json"):
                if os.path.exists(f"database/characters/{user_id}"):
                    # File will be overwritten, should it already exist
                    await message.attachments[0].save(fp=f"database/characters/{user_id}/{filename}")
                    if os.path.exists(f"database/characters/{user_id}/{filename}"):
                        await interaction.response.send_message("Bestehenden Charakter erfolgreich überschrieben!", ephemeral=True)
                    else:
                        await interaction.response.send_message("Charakter erfolgreich abgespeichert!", ephemeral=True)
                        
                else:
                    os.mkdir(f"database/characters/{user_id}")
                    await message.attachments[0].save(fp=f"database/characters/{user_id}/{filename}")
                    await interaction.response.send_message("Charakter erfolgreich abgespeichert!", ephemeral=True)
            else:
                await interaction.response.send_message("Falsches Format. Bitte nutze eine JSON-Datei!", ephemeral=True)
        else:
            await interaction.response.send_message("Keine Datei erkannt!", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(DSA(bot))
    print("DSA module loaded!")
