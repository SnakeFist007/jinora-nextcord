import nextcord
from nextcord import Interaction

class DrawButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @nextcord.ui.button(label="🎨", style=nextcord.ButtonStyle.green)
    async def sd_draw(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = 1
        self.stop()
        
    @nextcord.ui.button(label="📋", style=nextcord.ButtonStyle.blurple)
    async def sd_info(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = 2
        self.stop()
        
    @nextcord.ui.button(label="⚙️", style=nextcord.ButtonStyle.blurple)
    async def sd_settings(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = 3
        self.stop()