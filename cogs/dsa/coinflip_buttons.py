import random
import nextcord
from nextcord import Interaction

class Coinflip(nextcord.ui.View):
    def __init__(self):
        super().__init__()

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