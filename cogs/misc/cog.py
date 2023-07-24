import nextcord
import asyncio
import requests
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands
from main import logging, db_servers, url, parse_json, load_error_msg


def load_embed():
    defaults = parse_json("database/embeds/status_embed.json")
    return defaults

def convert_time(time):
    pos = ["s", "m", "h", "d", "min"]
    time_dict = {"s": 1, "m": 60, "h": 3600,
                "d": 86400, "min": 60}
    unit = time[-1]

    # TODO: Improve error handling
    # ! ERROR: Wrong / no unit given
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    # ! ERROR: Time is not an integer
    # TODO: Add actual Exception
    except:
        return -2

    return val * time_dict[unit] 

# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    # General stats of the bot
    @nextcord.slash_command(name="status", description="Pong!")
    async def status(self, interaction: Interaction):
        logging.info("Checking status...")
        # Get amount of servers joined
        count = db_servers.joined_servers_list.count_documents({})
        # Calculate latency
        ping = round(self.bot.latency * 1000)
        logging.info(f"Ping is {ping}ms.")
        # Check if Stable Diffusion is running
        try:
            requests.get(url=f"{url}/internal/ping")
            sd_status = "OK"
            logging.info("Stable Diffusion is online.")
        except Exception as e:
            sd_status = "Offline"
            logging.warning("Stable Diffusion is offline.")

        embed1 = load_embed()
        embed2 = {
            "description": f"Amount of Servers joined: `{count}`\nPing: `{ping}ms`\nStable Diffusion Status: `{sd_status}`"
        }
        em = Embed().from_dict(embed1 | embed2)

        await interaction.send(embed=em, ephemeral=True)


    # TODO: Create Autofeed view command
    @nextcord.slash_command()
    async def feeds(self, interaction: Interaction):
        pass
    
    # TODO: Interval picker or as Discord Modal
    @nextcord.slash_command()
    async def autofeed(self, interaction: Interaction, message: str = SlashOption(), interval: str = SlashOption(), channel: nextcord.TextChannel = SlashOption()):
        converted_time = convert_time(interval)
        
        # ! ERROR: wrong unit
        if converted_time == -1:
            em = load_error_msg()
            await interaction.response.send_message(embed=em, ephemeral=True)
            
        # ! ERROR: Integer Error
        elif converted_time == -2:
            em = load_error_msg()
            await interaction.response.send_message(embed=em, ephemeral=True)
            
        # * Create reminder
        else:
            # TODO: Autofeed command - sends a reminder every X days / X weeks / X months
            output = f"Reminder for `{message}` set! I'll remind you in `{interval}`."
            # Set reminder
            await interaction.send(f"{interaction.user.mention} {output}", ephemeral=False)
            await asyncio.sleep(converted_time)
            # Reminder triggered
            await interaction.send(f"{interaction.user.mention} Reminder: `{message}`", ephemeral=False)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
