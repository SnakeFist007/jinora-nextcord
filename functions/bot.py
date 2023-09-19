import nextcord
from nextcord.ext import commands


OWNER_ID = 83931378097356800

intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None, owner_id=OWNER_ID)
