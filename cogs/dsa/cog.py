import nextcord
import os
import shutil
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


    # Character Editors
    @nextcord.slash_command(name="character", description="Charakter-Optionen", guild_ids=[testServerID])
    async def character(self, interaction: Interaction):
        pass
                 
    @character.subcommand(name="download", description="Gibt den gespeicherten Charakter aus!")
    async def chars_download(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"
        
        if os.path.exists(path):
            file = nextcord.File(f"{path}/{str(user_id)}")
            await interaction.response.send_message("Dein gespeicherter Charakter!", file=file, ephemeral=True) 
                         
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
    

    @character.subcommand(name="delete", description="Löscht den gespeicherten Charakter!")
    async def char_del(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"  
        
        if os.path.exists(path):
            json_data = self.load_json()
            
            shutil.rmtree(path, ignore_errors=True)
            json_data.pop(str(user_id))
            self.save_json(json_data)
            
            await interaction.response.send_message("Alle gespeicherten Charaktere gelöscht!", ephemeral=True)               
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
        

    @nextcord.message_command(name="Charakter speichern")
    async def char_add(self, interaction: Interaction, message):
        user_id = interaction.user.id
        
        # FIXME: Newly posted messages will return an empty list too, despite having an attachement
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
