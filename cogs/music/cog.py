from time import time
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from nextcord.abc import GuildChannel
import wavelink
import datetime
import asyncio
from main import testServerID

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
        print(f"Node {node.identifier} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        interaction = player.interaction
        vc: player = interaction.guild.voice_client

        if vc.loop:
            return await vc.play(track)

        if vc.queue.is_empty:
            await interaction.send("Ende der Wartschleife erreicht!")
            return await vc.disconnect()
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        em = nextcord.Embed(
            title=f"Spiele {next_song.title} ab", description=f"Interpret: {next_song.author}")
        em.add_field(
            name="Länge", value=f"{str(datetime.timedelta(seconds=next_song.length))}")
        em.add_field(
            name="URL", value=f"[Klick mich!]({str(next_song.uri)})")

        await interaction.send(embed=em)

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

            em = nextcord.Embed(
                title=f"Spiele {vc.track.title} ab", description=f"Interpret: {vc.track.author}")
            em.add_field(
            name="Länge", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
            em.add_field(
                name="URL", value=f"[Klick mich!]({str(vc.track.uri)})")

            await interaction.send(embed=em)
        else:
            await vc.queue.put_wait(search)
            await interaction.send(f"***{search.title}*** der Wartschleife hinzugefügt!")

        vc.interaction = interaction
        setattr(vc, "loop", False)


    # SHOW CURRENT PLAYING VIDEO / SONG
    @nextcord.slash_command(name="nowplaying", description="Zeigt Informationen zum aktuell abgespielten Video an", guild_ids=[testServerID])
    async def nowplaying(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        
        em = nextcord.Embed(title=f"Spiele {vc.track.title} ab", description=f"Interpret: {vc.track.author}")
        em.add_field(name="Länge", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
        em.add_field(name="URL", value=f"[Klick mich!]({str(vc.track.uri)})")

        return await interaction.send(embed=em)


    # STOP PLAYBACK & DISCONNECT
    @nextcord.slash_command(name="stop", description="Stoppt die Wiedergabe", guild_ids=[testServerID])
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        
        await vc.stop()
        await vc.disconnect()
        await interaction.send("Stoppe die Wiedergabe!")


    # DISCONNECT (FOR DEBUG)
    @nextcord.slash_command(name="connect", description="Verbindet den Bot zum entsprechenden Kanal", guild_ids=[testServerID])
    async def connect(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Gewünschter Sprachkanal")):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
            await vc.connect(timeout=0, reconnect=False)
        else:
            return await interaction.send("Bereits verbunden!")       


    # DISCONNECT (FOR DEBUG)
    @nextcord.slash_command(name="disconnect", description="Trennt die Verbindung des Bots", guild_ids=[testServerID])
    async def disconnect(self, interaction: Interaction):
        vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.send("Tschüss!")


    # PAUSE PLAYBACK
    @nextcord.slash_command(name="pause", description="Pausiert das Video", guild_ids=[testServerID])
    async def pause(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.response.send_message("Pausiere das Video!")


    # RESUME PLAYBACK
    @nextcord.slash_command(name="resume", description="Resumes playback.", guild_ids=[testServerID])
    async def resume(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.response.send_message("Setzte das Video fort!")


    # SKIP VIDEO / SONG IN QUEUE OR DISCONNECT IF QUEUE IS EMPTY
    @nextcord.slash_command(name="skip", description="Überspringt das aktuelle Video", guild_ids=[testServerID])
    async def skip(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.queue.is_empty:
            await vc.stop()
            return await interaction.response.send_message("Video übersprungen!")
        else:
            await vc.stop()
            return await interaction.response.send_message("Video gestoppt!")


    # SET VOLUME (DEFAULT IS 50%)
    @nextcord.slash_command(name="volume", description="Lautstärke (0-150) einstellen", guild_ids=[testServerID])
    async def volume(self, interaction: Interaction, volume: int = SlashOption(description="Volume in % (1-150)")):
        if not interaction.guild.voice_client:
            return await interaction.send("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if volume > 251:
            await interaction.response.send_message("Bisschen viel Bruder.")
        if volume < 251 and volume > 101:
            await interaction.response.send_message("***Starting ear rape mode***")
            await interaction.response.send_message(f"Lautstärke auf {volume}% eingestellt!")
            return await vc.set_volume(volume)
        if volume < 101 and volume > 0:
            await interaction.response.send_message(f"Lautstärke auf {volume}% eingestellt!")
            return await vc.set_volume(volume)
        if volume < 0:
            await vc.disconnect()
            await interaction.response.send_message("Stelle auf stumm!")


    # LOOP PLAYBACK (TOGGLE COMMAND)
    @nextcord.slash_command(name="loop", description="Wiederholung an / aus schalten", guild_ids=[testServerID])
    async def loop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)
        
        if vc.loop:
            return await interaction.response.send_message("Wiederholung aktiviert!")
        else:
            return await interaction.response.send_message("Wiederholung deaktiviert!")


    # SHOW ALL VIDEOS / SONGS IN QUEUE
    @nextcord.slash_command(name="queue", description="Zeigt den Inhalt der Warteschleife", guild_ids=[testServerID])
    async def queue(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Es wird nichts abgespielt zur Zeit!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            return await interaction.response.send_message("Warteschleife ist leer!")

        em = nextcord.Embed(title="Aktuelle Warteschleife")
        queue = vc.queue.copy()
        song_count = 0

        for song in queue:
            song_count += 1
            em.add_field(name=f"**#{song_count}:** {song.title}", value=f"{str(song.uri)}", inline=False)

        return await interaction.send(embed=em)
            

def setup(bot):
    bot.add_cog(Music(bot))
    print("music.py cog loaded!")
