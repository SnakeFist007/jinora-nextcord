from time import time
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from nextcord.abc import GuildChannel
import wavelink
import datetime
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
            return await interaction.send("Reached end of queue!")
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        em = nextcord.Embed(
            title=f"Now playing {next_song.title}", description=f"Artist: {next_song.author}")
        em.add_field(
            name="Duration", value=f"{str(datetime.timedelta(seconds=next_song.length))}")
        em.add_field(
            name="URL", value=f"[Click Me!]({str(next_song.uri)})")

        await interaction.send(embed=em)


    # PLAY NEW VIDEO / SONG
    @nextcord.slash_command(name="play", description="Plays a YouTube video.", guild_ids=[testServerID])
    async def play(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Voice Channel to join"), search: str = SlashOption(description="Video URL or name")):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)

            em = nextcord.Embed(
                title=f"Now playing {vc.track.title}", description=f"Artist: {vc.track.author}")
            em.add_field(
            name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
            em.add_field(
            name="URL", value=f"[Click Me!]({str(vc.track.uri)})")

            await interaction.send(embed=em)
        else:
            await vc.queue.put_wait(search)
            await interaction.send(f"Added ***{search.title}*** to the queue!")

        vc.interaction = interaction
        setattr(vc, "loop", False)


    # SHOW CURRENT PLAYING VIDEO / SONG
    @nextcord.slash_command(name="nowplaying", description="Shows the name of the current track.", guild_ids=[testServerID])
    async def nowplaying(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.send("There is nothing playing at the moment!")
        
        em = nextcord.Embed(title=f"Now playing {vc.track.title}", description=f"Artist: {vc.track.author}")
        em.add_field(name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
        em.add_field(name="URL", value=f"[Click Me!]({str(vc.track.uri)})")

        return await interaction.send(embed=em)


    # STOP PLAYBACK & DISCONNECT
    @nextcord.slash_command(name="stop", description="Stops playback & disconnects the bot from any voice channel.", guild_ids=[testServerID])
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        
        await vc.stop()
        await vc.disconnect()
        await interaction.send("Stopping playback!")


    # DISCONNECT (FOR DEBUG)
    @nextcord.slash_command(name="connect", description="Connects the bot to a channel.", guild_ids=[testServerID])
    async def connect(self, interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Voice Channel to join")):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
            await vc.connect(timeout=0, reconnect=False)
            await interaction.send("Connecting!", ephemeral=True)
        else:
            return await interaction.send("Already connected! Please disconnect / stop the current running instance first.")       


    # DISCONNECT (FOR DEBUG)
    @nextcord.slash_command(name="disconnect", description="Disconnects the bot from any voice channel.", guild_ids=[testServerID])
    async def disconnect(self, interaction: Interaction):
        vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.send("Disconnecting!")


    # PAUSE PLAYBACK
    @nextcord.slash_command(name="pause", description="Pauses playback.", guild_ids=[testServerID])
    async def pause(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.send("Pausing playback!")


    # RESUME PLAYBACK
    @nextcord.slash_command(name="resume", description="Resumes playback.", guild_ids=[testServerID])
    async def resume(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.send("Resuming playback!")


    # SKIP VIDEO / SONG IN QUEUE OR DISCONNECT IF QUEUE IS EMPTY
    @nextcord.slash_command(name="skip", description="Skips the current song.", guild_ids=[testServerID])
    async def skip(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.queue.is_empty:
            await vc.stop()
            return await interaction.send("Skipping current video / song!")
        else:
            await vc.stop()
            return await interaction.send("Stopping currently running track, disconnecting!")


    # SET VOLUME (DEFAULT IS 50%)
    @nextcord.slash_command(name="volume", description="Set the playback volume (0-150).", guild_ids=[testServerID])
    async def volume(self, interaction: Interaction, volume: int = SlashOption(description="Volume in % (1-150)")):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if volume > 251:
            await interaction.send("That's a little much bruh")
        if volume < 251 and volume > 101:
            await interaction.send("Let's go into earrape mode")
            await interaction.send(f"Setting the volume to {volume}%")
            return await vc.set_volume(volume)
        if volume < 101 and volume > 0:
            await interaction.send(f"Setting the volume to {volume}%")
            return await vc.set_volume(volume)
        if volume < 0:
            await interaction.send("Can't go that low. You wouldn't hear anything anyway then.")


    # LOOP PLAYBACK (TOGGLE COMMAND)
    @nextcord.slash_command(name="loop", description="Toggle looping the playback.", guild_ids=[testServerID])
    async def loop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)
        
        if vc.loop:
            return await interaction.send("Repeat is now enabled!")
        else:
            return await interaction.send("Repeat is now disabled!")


    # SHOW ALL VIDEOS / SONGS IN QUEUE
    @nextcord.slash_command(name="queue", description="Shows the content of the current queue.", guild_ids=[testServerID])
    async def queue(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("There is nothing playing at the moment!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            return await interaction.send("Queue is empty!")

        em = nextcord.Embed(title="Current Queue")
        queue = vc.queue.copy()
        song_count = 0

        for song in queue:
            song_count += 1
            em.add_field(name=f"**#{song_count}:** {song.title}", value=f"{str(song.uri)}", inline=False)

        return await interaction.send(embed=em)
            

def setup(bot):
    bot.add_cog(Music(bot))
    print("music.py cog loaded!")
