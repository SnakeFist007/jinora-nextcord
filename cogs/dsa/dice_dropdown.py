import random
import nextcord
from nextcord import Interaction
from typing import Optional

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

class DiceDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DiceDropdown())