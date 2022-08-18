import nextcord
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
    async def char_add(self, interaction: Interaction):
        await interaction.response.send_message("Bitte nutze Optolith um einen Charakter zu erstellen und lade anschließend die JSON-Datei als Antwort auf diese Nachricht hoch!", ephemeral=True)
        
        def check(m: nextcord.Message):
            return m.user.id == interaction.user.id and m.channel.id == interaction.channel.id 

        reply = await self.bot.wait_for("message", check=check)
        
        if not str(reply.attachments) == "[]":
            # Get the filename
            split_v1 = str(reply.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            
            if filename.endswith(".json"):
                await reply.attachments[0].save(fp=f"database/characters/{reply.user.id}/{filename}")
                
            else:
                await interaction.response.send_message("Falsches Format. Bitte sende mir eine JSON-Datei!", ephemeral=True)
        else:
            await interaction.response.send_message("Bitte sende mir eine JSON-Datei als Anhang!", ephemeral=True)
            
        
        # TODO: Implement file upload to bot, check for json file format and optolith formatting
        # Create new folder for each unique Discord-ID, limit amount of total saved characters to 10, total file size to 8 MB
        # Place JSON inside Unique-ID folder and add name to the db_characters.json
        pass
           
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
        # TODO: Clear all saved characters
        pass


# Add Cog to bot
def setup(bot):
    bot.add_cog(DSA(bot))
    print("DSA module loaded!")
