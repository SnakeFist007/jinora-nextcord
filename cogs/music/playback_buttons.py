import nextcord
import wavelink
from nextcord import Interaction

class ControlPanel(nextcord.ui.View):
    def __init__(self, vc, interaction: Interaction):
        super().__init__()
        self.vc = vc
        self.ctx = interaction
    

    @nextcord.ui.button(label="Play/Pause", emoji="⏯️", style=nextcord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.clear_reaction(emoji="⏸️")
        else:
            await self.vc.pause()
            await interaction.message.add_reaction(emoji="⏸️")


    @nextcord.ui.button(label="Loop", emoji="🔁", style=nextcord.ButtonStyle.blurple)
    async def loop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            self.vc.loop ^= True
            if self.vc.loop:
                await interaction.message.add_reaction(emoji="🔁")
            else:
                await interaction.message.clear_reaction(emoji="🔁")
        except Exception:
            setattr(self.vc, "loop", False)
    

    @nextcord.ui.button(label="Skip", emoji="⏭️", style=nextcord.ButtonStyle.blurple)
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.vc.queue.is_empty:
            await self.vc.stop()
            await self.vc.disconnect()
            await interaction.message.delete()

        try:
            await self.vc.seek(self.vc.track.length * 1000)
            if self.vc.is_paused():
                await self.vc.resume()

            await interaction.response.send_message("Spiele den nächsten Track!", ephemeral=True)
            
        except wavelink.errors.QueueEmpty:
            return await interaction.response.send_message("Die Warteschlange ist leer!", ephemeral=True)
        
        except AttributeError:
            pass
    

    @nextcord.ui.button(label="Queue", emoji="#️⃣", style=nextcord.ButtonStyle.blurple)
    async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):   
        em = nextcord.Embed(title="🐍 Schlange 🐍")
        em.add_field(name=f"***Aktueller Track***", value=f"**{self.vc.track.title}**", inline=False)

        if not self.vc.queue.is_empty:
            queue = self.vc.queue.copy()
            song_count = 0
            
            for song in queue:
                song_count += 1
                em.add_field(name=f"**#{song_count}:** {song.title}", value=f"{str(song.uri)}", inline=False)

        return await interaction.response.send_message(embed=em, ephemeral=True)


    @nextcord.ui.button(label="Stop", emoji="⏏️", style=nextcord.ButtonStyle.red)
    async def disconnect(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.vc.disconnect()
        await interaction.message.delete()