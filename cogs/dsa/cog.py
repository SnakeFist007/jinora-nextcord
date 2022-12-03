import nextcord
import os
import shutil
import aiosqlite
import requests
import zipfile
import json
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from typing import Optional
from .dice_dropdown import DiceDropdownView
from .coinflip_buttons import Coinflip
from main import db_characters

# Initialize Cog
class DSA(commands.Cog, name="DSA"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    # DICE COMMAND HANDLER
    @nextcord.slash_command(name="dice", description="Verschiedene Würfel-Optionen")
    async def dice(self, interaction: Interaction):
        pass
    
    
    # Slash Command: Throw a dice selected from a dropdown menu
    @dice.subcommand(name="roll", description="Würfel werfen!")
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)
    
    
    # Slash Command: Throw one or multiple dice after a regex input
    @dice.subcommand(name="multi", description="Mehrere Würfel werfen!")
    async def dice_multiple(self, interaction: Interaction, dice: Optional[str] = SlashOption(name="")):
        pass
    
        # TODO: Think of a easily extensible dice roll format, parsable by regex
        # def roll(match):
        #     a,b = match.group(1).split('d')
        #     return str(random.randint(int(a), int(a)*int(b)))

        # re.sub('(\d+d\d+)', roll, dice)
        
    
    
    # COIN-FLIP COMMAND HANDLER
    @nextcord.slash_command(name="coin", description="Verschiedene Münz-Werf-Optionen")
    async def coin(self, interaction: Interaction):
        pass


    # Slash Command: Flip a coin
    @coin.subcommand(name="flip", description="Wirf eine Münze!")
    async def coin_flip(self, interaction: Interaction):
        await interaction.send(view=Coinflip(), ephemeral=True)



    # DSA COMMAND HANDLER
    @nextcord.slash_command(name="character", description="Charakter-Optionen")
    async def dsa(self, interaction: Interaction):
        pass
    
    
    # Slash Command: List all saved characters of a user
    @dsa.subcommand(name="list", description="Zeigt eine Liste aller gespeicherten Charaktere an!")
    async def dsa_chars_list(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/char_storage/{user_id}"
        dir_list = os.listdir(path)
        count = 0
        
        em = nextcord.Embed(title="Gespeicherte Charaktere")
        
        for entry in dir_list:
            count += 1
            em.add_field(name=f"**#{count}**", value=f"{entry}", inline=False)
            
        return await interaction.response.send_message(embed=em, ephemeral=True)


    # TODO: optimally with dropdown menu
    # Slash Command: Send json-file of a saved character as a Discord message to the user
    @dsa.subcommand(name="download", description="Gibt den ausgewählten Charakter als Datei aus!")
    async def dsa_chars_download(self, interaction: Interaction, character: str):
        user_id = interaction.user.id
        path = f"database/char_storage/{user_id}/{character}.json"
        
        if os.path.exists(path):
            file = nextcord.File(path)
            await interaction.response.send_message(f"Dein gespeicherter Charakter: {character}!", file=file, ephemeral=True)         
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
    
    
    # TODO: optimally with dropdown menu
    # Slash Command: Delete a selected character of the user
    @dsa.subcommand(name="delete", description="Löscht den ausgewählten Charakter!")
    async def dsa_char_del(self, interaction: Interaction, character: str):
        user_id = interaction.user.id
        path = f"database/char_storage/{user_id}"
        file = f"{path}/{character}.json"
        
        # Check if user has saved characters
        if os.path.exists(path):
            
            # Check if user has saved that specific character
            if os.path.exists(file):
                os.remove(file)
                
                # Remove DB entry
                async with aiosqlite.connect(db_characters) as db:
                    async with db.cursor() as cursor:
                        await cursor.execute(f"DELETE FROM characters WHERE char_name LIKE {character}")
                    await db.commit()
                await interaction.response.send_message(f"{character} gelöscht!", ephemeral=True)  
                    
            else:
                await interaction.response.send_message("Charakter nicht gefunden!", ephemeral=True)     
                                     
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
    
    
    # Slash Command: Delete all saved characters for the user
    @dsa.subcommand(name="reset", description="Löscht ALLE gespeicherten Charaktere!")
    async def dsa_char_delAll(self, interaction: Interaction):
        user_id = interaction.user.id
        path = f"database/char_storage/{user_id}"  
        
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True) 
            
            # Remove DB entry
            async with aiosqlite.connect(db_characters) as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f"DELETE FROM characters WHERE user LIKE {user_id}")
                await db.commit()
            await interaction.response.send_message("Alle gespeicherten Charaktere gelöscht!", ephemeral=True)  
                       
        else:
            await interaction.response.send_message("Keine Charaktere gespeichert!", ephemeral=True)
        
    
    # Slash Command: Delete all saved characters for the user
    @dsa.subcommand(name="add", description="Fügt einen neuen Charakter hinzu!")
    async def dsa_char_add(self, interaction: Interaction, char_name: str, file: nextcord.Attachment):
        user_id = interaction.user.id
        
        if file.filename.endswith(".json"):
            path = f"database/char_storage/{user_id}"
            store_json = f"{path}/{char_name}.json"
            
            if not os.path.exists(path):
                os.mkdir(path)
            
            with open(store_json, "w") as f:
                json.dump(requests.get(file).json(), f)
            
            # Create DB entry
            async with aiosqlite.connect(db_characters) as db:
                async with db.cursor() as cursor:
                    params = (user_id, char_name, store_json)
                    await cursor.execute(f"INSERT INTO characters VALUES (?,?,?)", params)
                await db.commit()
            await interaction.response.send_message("Charakter erfolgreich gespeichert!", ephemeral=True)
            
        else:
            await interaction.response.send_message("Bitte als json-Datei hochladen!", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(DSA(bot))
    print("DSA module loaded!")
