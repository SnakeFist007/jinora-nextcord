import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import wavelink
import json
import validators
from main import testServerID
from .playback_buttons import ControlPanel

# Initialize Cog
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        default_server = 2
        backup_server = 1
        music_json = "database/db_lavalink.json"

        with open(music_json) as f:
            data = json.load(f)
        
        await self.bot.wait_until_ready()

        # Try to connect to primary server
        try:
            server = "server_" + str(default_server)
        
            await wavelink.NodePool.create_node(
                bot=self.bot, 
                host=data[server]["host"], 
                port=data[server]["port"], 
                password=data[server]["password"], 
                https=data[server]["https"])

        # Use backup server if it fails
        except:
            server = "server_" + str(backup_server)
        
            await wavelink.NodePool.create_node(
                bot=self.bot, 
                host=data[server]["host"], 
                port=data[server]["port"], 
                password=data[server]["password"], 
                https=data[server]["https"])


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
        
        except wavelink.errors.QueueEmpty:
            return await vc.disconnect()


    # PLAY NEW VIDEO
    @nextcord.slash_command(name="play", description="Spielt ein YouTube Video ab", guild_ids=[testServerID])
    async def play(self, interaction: Interaction, search: str = SlashOption(description="Video URL or name")):
        video = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        try:            
            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = interaction.guild.voice_client

        except AttributeError:
            return await interaction.response.send_message("Tritt zuerst einem Sprachkanal bei!", ephemeral=True)

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(video)
            
            em = nextcord.Embed(title=f"🎶 Musik-Steuerungstafel 🎶", color=0x3498db)
            view = ControlPanel(vc, interaction)
            
            await interaction.send(embed=em, view=view)
            
        else:
            await vc.queue.put_wait(video)
            await interaction.response.send_message(f"***{video.title}*** der Wartschleife hinzugefügt!",ephemeral=True)

        vc.interaction = interaction
        setattr(vc, "loop", False)

    # CONTEXT MENU PLAY        
    @nextcord.message_command(name="Mit Lene abspielen")
    async def play_context(self, interaction: Interaction, message):        
        if validators.url(message.content):
            video = await wavelink.YouTubeTrack.search(query=message.content, return_first=True)
            
            try:            
                if not interaction.guild.voice_client:
                    vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
                else:
                    vc: wavelink.Player = interaction.guild.voice_client

            except AttributeError:
                return await interaction.response.send_message("Tritt zuerst einem Sprachkanal bei!", ephemeral=True)

            if vc.queue.is_empty and not vc.is_playing():
                await vc.play(video)
                
                em = nextcord.Embed(title=f"🎶 Musik-Spieler 🎶", color=0x3498db)
                view = ControlPanel(vc, interaction)
                
                await interaction.send(embed=em, view=view)
                
            else:
                await vc.queue.put_wait(video)
                await interaction.response.send_message(f"***{video.title}*** der Wartschleife hinzugefügt!",ephemeral=True)

            vc.interaction = interaction
            setattr(vc, "loop", False)
            
        else:
            await interaction.response.send_message("Bitte eine Nachricht auswählen, die nur eine URL beinhält!", ephemeral=True)


    # DISCONNECT (RESET-COMMAND)
    @nextcord.slash_command(name="reset", description="Trennt die Verbindung des Bots", guild_ids=[testServerID])
    @application_checks.has_permissions(moderate_members=True)
    async def music_reset(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Nicht verbunden!", ephemeral=True)  

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.stop()
            await vc.disconnect()  
            await interaction.response.send_message("Setze Bot zurück!", ephemeral=True)                                                                                                 
            

# Add Cog to bot
def setup(bot):
    bot.add_cog(Music(bot))
    print("Music module loaded!")