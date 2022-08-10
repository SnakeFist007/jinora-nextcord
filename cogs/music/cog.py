from time import time
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from nextcord.abc import GuildChannel
import wavelink
import datetime
from main import testServerID
from .playback_buttons import ControlPanel

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalinkinc.ml", port=443, password="incognito", https=True)

    # Events
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"\tMusic-Mode #{node.identifier} is ready!\n")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        interaction = player.interaction
        vc: player = interaction.guild.voice_client

        if vc.loop:
            return await vc.play(track)

        try:
            next_song = vc.queue.get()
            await vc.play(next_song)

            # FETCH ID FROM PANEL MESSAGE -> UPDATE MESSAGE
            # em = nextcord.Embed(title=f"Spiele {next_song.title} ab", description=f"Interpret: {next_song.author}")
            # em.add_field(name="Länge", value=f"{str(datetime.timedelta(seconds=next_song.length))}")
            # em.add_field(name="URL", value=f"[Klick mich!]({str(next_song.uri)})")
            # await interaction.message.edit(embed=em)
        
        except wavelink.errors.QueueEmpty:
            return await vc.disconnect()


    # PLAY NEW VIDEO / SONG
    @nextcord.slash_command(name="play", description="Spielt ein YouTube Video ab", guild_ids=[testServerID])
    async def play(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Voice Channel to join"), search: str = SlashOption(description="Video URL or name")):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)

            em = nextcord.Embed(title=f"Spiele {vc.track.title} ab", description=f"Kanal: {vc.track.author}")
            em.add_field(name="Länge", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
            em.add_field(name="URL", value=f"[Klick mich!]({str(vc.track.uri)})")
            
            view = ControlPanel(vc, interaction)

            await interaction.send(embed=em, view=view)
            
        else:
            await vc.queue.put_wait(search)
            await interaction.response.send_message(f"***{search.title}*** der Wartschleife hinzugefügt!",ephemeral=True)

        vc.interaction = interaction
        setattr(vc, "loop", False)


    # STOP PLAYBACK & DISCONNECT
    @nextcord.slash_command(name="stop", description="Stoppt die Wiedergabe", guild_ids=[testServerID])
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        
        await vc.stop()
        await vc.disconnect()
        await interaction.send("Stoppe die Wiedergabe!")


    # DISCONNECT (FOR DEBUG)
    # @nextcord.slash_command(name="connect", description="Verbindet den Bot zum entsprechenden Kanal", guild_ids=[testServerID])
    # async def connect(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Gewünschter Sprachkanal")):
    #     if not interaction.guild.voice_client:
    #         vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
    #         await vc.connect(timeout=0, reconnect=False)
    #     else:
    #         return await interaction.response.send_message("Bereits verbunden!", ephemeral=True)       


    # DISCONNECT (FOR DEBUG)
    # @nextcord.slash_command(name="disconnect", description="Trennt die Verbindung des Bots", guild_ids=[testServerID])
    # async def disconnect(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Nicht verbunden!", ephemeral=True)  

    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client
    #         await vc.disconnect()  
    #         await interaction.send("Tschüss!")


    # PAUSE PLAYBACK
    # @nextcord.slash_command(name="pause", description="Pausiert das Video", guild_ids=[testServerID])
    # async def pause(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)

    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client

    #     await vc.pause()
    #     await interaction.send("Pausiere das Video!")


    # RESUME PLAYBACK
    # @nextcord.slash_command(name="resume", description="Resumes playback.", guild_ids=[testServerID])
    # async def resume(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)
    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client

    #     await vc.resume()
    #     await interaction.send("Setzte das Video fort!")

    # SKIP VIDEO / SONG IN QUEUE OR DISCONNECT IF QUEUE IS EMPTY
    # @nextcord.slash_command(name="skip", description="Überspringt das aktuelle Video", guild_ids=[testServerID])
    # async def skip(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)
    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client

    #     if not vc.queue.is_empty:
    #         await vc.stop()
    #         return await interaction.send("Video übersprungen!")
    #     else:
    #         await vc.stop()
    #         return await interaction.send("Video gestoppt!")

    # LOOP PLAYBACK (TOGGLE COMMAND)
    # @nextcord.slash_command(name="loop", description="Wiederholung an / aus schalten", guild_ids=[testServerID])
    # async def loop(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)
    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client

    #     try:
    #         vc.loop ^= True
    #     except Exception:
    #         setattr(vc, "loop", False)
        
    #     if vc.loop:
    #         return await interaction.send("Wiederholung aktiviert!")
    #     else:
    #         return await interaction.send("Wiederholung deaktiviert!")


    # SHOW ALL VIDEOS / SONGS IN QUEUE
    # @nextcord.slash_command(name="queue", description="Zeigt den Inhalt der Warteschleife", guild_ids=[testServerID])
    # async def queue(self, interaction: Interaction):
    #     if not interaction.guild.voice_client:
    #         return await interaction.response.send_message("Es wird zur Zeit nichts abgespielt!", ephemeral=True)
    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client

    #     if vc.queue.is_empty:
    #         return await interaction.response.send_message("Warteschleife ist leer!", ephemeral=True)

    #     em = nextcord.Embed(title="Aktuelle Warteschleife")
    #     queue = vc.queue.copy()
    #     song_count = 0

    #     for song in queue:
    #         song_count += 1
    #         em.add_field(name=f"**#{song_count}:** {song.title}", value=f"{str(song.uri)}", inline=False)

    #     return await interaction.send(embed=em)
            

def setup(bot):
    bot.add_cog(Music(bot))
    print("Music module loaded!")