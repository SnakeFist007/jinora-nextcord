import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from main import testServerID
import random

class DiceDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="D4", emoji="🎲",
                                  description="Wift einen 4-seitigen Würfel."),
            nextcord.SelectOption(label="D6", emoji="🎲",
                                  description="Wift einen 6-seitigen Würfel."),
            nextcord.SelectOption(label="D8", emoji="🎲",
                                  description="Wift einen 8-seitigen Würfel."),
            nextcord.SelectOption(label="D10", emoji="🎲",
                                  description="Wift einen 10-seitigen Würfel."),
            nextcord.SelectOption(label="D12", emoji="🎲",
                                  description="Wift einen 12-seitigen Würfel."),
            nextcord.SelectOption(label="D20", emoji="🎲",
                                  description="Wift einen 20-seitigen Würfel.")
        ]
        super().__init__(placeholder="Würfel-Größe auswählen...",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "D4":
            await interaction.response.send_message(f"`{random.randint(1,4)}` wurde gewürfelt!", ephemeral=False)
        elif self.values[0] == "D6":
            await interaction.response.send_message(f"`{random.randint(1,6)}` wurde gewürfelt!", ephemeral=False)
        elif self.values[0] == "D8":
            await interaction.response.send_message(f"`{random.randint(1,8)}` wurde gewürfelt!", ephemeral=False)
        elif self.values[0] == "D10":
            await interaction.response.send_message(f"`{random.randint(1,10)}` wurde gewürfelt!", ephemeral=False)
        elif self.values[0] == "D12":
            await interaction.response.send_message(f"`{random.randint(1,12)}` wurde gewürfelt!", ephemeral=False)
        elif self.values[0] == "D20":
            await interaction.response.send_message(f"`{random.randint(1,20)}` wurde gewürfelt!", ephemeral=False)
        else:
            await interaction.response.send_message("Bitte einen gültigen Einstieg wählen!", ephemeral=True)

class Coinflip(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Kopf", style=nextcord.ButtonStyle.blurple)
    async def coin_heads(self, button: nextcord.ui.Button, interaction: Interaction):
        flipped_coin = random.randint(0,1)
        if flipped_coin == 0:
            await interaction.response.send_message("`Kopf`! Du hast gewonnen!", ephemeral=False)
        else:
            await interaction.response.send_message("`Zahl`! Du hast verloren!", ephemeral=False)

    @nextcord.ui.button(label="Zahl", style=nextcord.ButtonStyle.blurple)
    async def coin_tails(self, button: nextcord.ui.Button, interaction: Interaction):
        flipped_coin = random.randint(0,1)
        if flipped_coin == 1:
            await interaction.response.send_message("`Zahl`! Du hast gewonnen!", ephemeral=False)
        else:
            await interaction.response.send_message("`Kopf`! Du hast verloren!", ephemeral=False)


class DiceDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DiceDropdown())


# Initialize Cog
class DSA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="roll", description="Würfel werfen!", guild_ids=[testServerID])
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="coinflip", description="Wirf eine Münze!", guild_ids=[testServerID])
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
