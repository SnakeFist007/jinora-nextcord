import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands, application_checks
import wavelink
import json
import validators
from .playback_buttons import ControlPanel

# Initialize Cog
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())
    
    # Connect to wavelink server, to be able to playback YouTube videos (2 servers configured)            
    async def node_connect(self):
        async def try_connect_wavelink(server_data):
            await wavelink.NodePool.create_node(
                    bot=self.bot, 
                    host=data[server_data]["host"], 
                    port=data[server_data]["port"], 
                    password=data[server_data]["password"], 
                    https=data[server_data]["https"])
        default_server = 2
        backup_server = 1
        
        # Load json file with login data
        music_json = "database/db_lavalink.json"
        with open(music_json) as f:
            data = json.load(f)
               
        # Wait until the bot is ready, then proceed
        await self.bot.wait_until_ready()
  
        # Try to connect to primary server
        try:
            server = "server_" + str(default_server)
            await try_connect_wavelink(server)
        # Use backup server if primary not available
        except:
            server = "server_" + str(backup_server)
            await try_connect_wavelink(server)


    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"\tMusic-Mode #{node.identifier} is ready!\n")

    # Queue handeling: Disconnect if empty, else play the next song
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

    
    
    # MUSIC COMMAND HANDLER
    @nextcord.slash_command(name="music", description="Verschiedene Musik-Optionen")
    async def music(self, interaction: Interaction):
        pass
    
    
    # Slash Command: Play YouTube video (either through URL or search term)
    @music.subcommand(name="play", description="Spielt ein YouTube Video ab")
    async def music_play(self, interaction: Interaction, search: str = SlashOption(description="Video URL or name")):
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
            await interaction.response.send_message(f"***{video.title}*** der Wartschleife hinzugefügt!", ephemeral=True)

        vc.interaction = interaction
        setattr(vc, "loop", False)


    # Context Menu Command: Play YouTube video through URL in message. ONLY WORKS WITH PURE URL MESSAGES!    
    @nextcord.message_command(name="Mit Lene abspielen")
    async def context_play(self, interaction: Interaction, message):
        # Check if message just contains a valid URL        
        if validators.url(message.content):
            video = await wavelink.YouTubeTrack.search(query=message.content, return_first=True)
            
            try:            
                if not interaction.guild.voice_client:
                    vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
                else:
                    vc: wavelink.Player = interaction.guild.voice_client

            # Catch excpetion if user is not connected to a channel
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

            # Clear loop state
            await interaction.message.clear_reaction(emoji="🔁")
            vc.interaction = interaction
            setattr(vc, "loop", False)
            
        # Give error if theres text / invalid URL in the message
        else:
            await interaction.response.send_message("Bitte eine Nachricht auswählen, die **nur** eine __gültige__ URL beinhält!", ephemeral=True)


    # Slash Command: Resets the bot, should there be any error / control-panel not showing up
    @music.subcommand(name="reset", description="Trennt die Verbindung des Bots")
    @application_checks.has_permissions(moderate_members=True)
    async def music_reset(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Nicht verbunden!", ephemeral=True)  

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            # Clear queue, stop playback and disconnect the bot
            vc.queue.clear()
            await vc.stop()
            await vc.disconnect()
            await interaction.response.send_message("Setze die Wiedergabe zurück!", ephemeral=True)                                                                                             
            

# Add Cog to bot
def setup(bot):
    bot.add_cog(Music(bot))
    print("Music module loaded!")