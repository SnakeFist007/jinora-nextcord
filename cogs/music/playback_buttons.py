import nextcord
from nextcord import Interaction

class ControlPanel(nextcord.ui.View):
    def __init__(self, vc, interaction: Interaction):
        super().__init__()
        self.vc = vc
        self.ctx = interaction
    
    @nextcord.ui.button(label="Resume/Pause", style=nextcord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.edit(content="**Status:** Wiedergabe fortgesetzt", view=self)
        else:
            await self.vc.pause()
            await interaction.message.edit(content="**Status:** Pausiert!", view=self)


    @nextcord.ui.button(label="Queue", style=nextcord.ButtonStyle.blurple)
    async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("Die Warteschlange ist leer!", ephemeral=True)
    
        em = nextcord.Embed(title="Queue")
        queue = self.vc.queue.copy()
        songCount = 0

        for song in queue:
            songCount += 1
            em.add_field(name=f"Song Num {str(songCount)}", value=f"`{song}`")
        await interaction.message.edit(embed=em, view=self)
    

    @nextcord.ui.button(label="Skip", style=nextcord.ButtonStyle.blurple)
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("Die Warteschlange ist leer! Zum Beenden bitte den 'Stop'-Knopf nutzen!", ephemeral=True)

        try:
            next_song = self.vc.queue.get()
            await self.vc.play(next_song)
            await interaction.message.edit(content=f"**Status:** Spielt `{next_song}` ab.", view=self)
        except Exception:
            return await interaction.response.send_message("Die Warteschlange ist leer!", ephemeral=True)
    

    @nextcord.ui.button(label="Stop", style=nextcord.ButtonStyle.red)
    async def disconnect(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        await interaction.message.delete()