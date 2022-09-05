import nextcord
import os
import shutil
import re
import random
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
        
    # DICE COMMAND HANDLER
    @nextcord.slash_command(name="dice", description="Verschiedene Würfel-Optionen", guild_ids=[testServerID])
    async def dice(self, interaction: Interaction):
        pass
    
    # Slash Command: Throw a dice selected from a dropdown menu
    @dice.subcommand(name="roll", description="Würfel werfen!")
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)
    
    # Slash Command: Throw one or multiple dice after a regex input
    @dice.subcommand(name="multi", description="Mehrere Würfel werfen!")
    async def dice_multiple(self, interaction: Interaction, dice: Optional[str] = SlashOption(name="")):
        # TODO: Think of a easily extensible dice roll format, parsable by regex
        pass
        # def roll(match):
        #     a,b = match.group(1).split('d')
        #     return str(random.randint(int(a), int(a)*int(b)))

        # re.sub('(\d+d\d+)', roll, dice)
        
       
    # COIN-FLIP COMMAND HANDLER
    @nextcord.slash_command(name="coin", description="Verschiedene Münz-Werf-Optionen", guild_ids=[testServerID])
    async def coin(self, interaction: Interaction):
        pass

    # Slash Command: Flip a coin
    @coin.subcommand(name="flip", description="Wirf eine Münze!")
    async def coin_flip(self, interaction: Interaction):
        await interaction.send(view=Coinflip(), ephemeral=True)


    # CHARACTER COMMAND HANDLER
    @nextcord.slash_command(name="character", description="Charakter-Optionen", guild_ids=[testServerID])
    async def character(self, interaction: Interaction):
        pass
    
    # Slash Command: List all saved characters of a user
    @character.subcommand(name="list", description="Zeigt eine Liste aller gespeicherten Charaktere an!")
    async def chars_list(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"
        dir_list = os.listdir(path)
        count = 0
        
        em = nextcord.Embed(title="Gespeicherte Charaktere")
        
        for entry in dir_list:
            count += 1
            em.add_field(name=f"**#{count}**", value=f"{entry}", inline=False)
            
        return await interaction.response.send_message(embed=em, ephemeral=True)

    # Slash Command: Send json-file of a saved character as a Discord message to the user
    @character.subcommand(name="download", description="Gibt den ausgewählten Charakter als Datei aus!")
    async def chars_download(self, interaction: Interaction, character: Optional[str] = SlashOption()):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}/{character}.json"
        
        if os.path.exists(path):
            file = nextcord.File(path)
            await interaction.response.send_message(f"Dein gespeicherter Charakter: {character}!", file=file, ephemeral=True) 
                         
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
    
    # Slash Command: Delete a selected character of the user (optimally with dropdown menu)
    @character.subcommand(name="delete", description="Löscht den ausgewählten Charakter!")
    async def char_del(self, interaction: Interaction, character: Optional[str] = SlashOption()):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"
        file = f"{path}/{character}.json"
        
        if os.path.exists(path):
            if os.path.exists(file):
                os.remove(file)
                await interaction.response.send_message(f"{character} gelöscht!", ephemeral=True)
                
            else:
                await interaction.response.send_message("Keinen Charakter gefunden!", ephemeral=True)              
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
    
    # Slash Command: Delete all saved characters for the user
    @character.subcommand(name="reset", description="Löscht ALLE gespeicherten Charaktere!")
    async def char_del_all(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/characters/{user_id}"  
        
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            await interaction.response.send_message("Alle gespeicherten Charaktere gelöscht!", ephemeral=True)    
                       
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
        
    # Context Menu Command: Save json file from sent message (grab attachement)
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
