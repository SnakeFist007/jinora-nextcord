import nextcord
import requests
import io
import base64
import os
import json
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands
from typing import Optional
from PIL import Image
from main import logging, url, db_stablediffusion

def prepare_directory():
    if not os.path.exists("cogs/stablediffusion/tmp"):
        os.makedirs("cogs/stablediffusion/tmp")
        logging.warning("Temporary image directory missing! Creating a new one...")


def load_defaults():
    with open("database\\stable_diffusion\\bot_settings.json", "r") as json_file:
        defaults = json.load(json_file)
    
    return defaults

def load_embed():
    with open("database\\embeds\\sd_embed.json", "r") as json_file:
        defaults = json.load(json_file)
        
    return defaults

tmp_path = "cogs/stablediffusion/tmp"
    
# Initialize Cog
class StableDiffusion(commands.Cog, name="StableDiffusion"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    # Generate
    @nextcord.slash_command(name="generate", description="Generates a picture! (txt2img)")
    async def sd_generate(
        self, interaction: Interaction, 
        prompt: str = SlashOption(description="Insert your prompt"), 
        negative_prompt: Optional[str] = SlashOption(description="Insert your negative prompt", required=False, default="")):
        
        await interaction.response.defer()
        logging.info("Recieving Stable Diffusion txt2img instruction...")
        message = await interaction.channel.fetch_message(int(interaction.channel.last_message_id))
        
        prepare_directory()
        defaults = load_defaults()
        user_input = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        prt_payload = defaults | user_input
        
        # Send request to Stable Diffusion API
        try:
            res = requests.post(url=f"{url}/sdapi/v1/txt2img", json=prt_payload)
            logging.info(f"Sending prompt payload to {url}.")
        except ConnectionError:
            logging.exception("Stable Diffusion Server is offline!")
            await interaction.channel.send("I'm very sorry to say this, but I can't generate images at the moment!")
            await message.delete()
        except Exception as e:
            logging.exception(e)
            await interaction.channel.send("I'm very sorry to say this, but I can't generate images at the moment!")
            await message.delete()
        
        # Extract image and prepare for Discord
        r = res.json()
        for i in r["images"]:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            image.save(f"{tmp_path}/output.png")
            logging.info(f"Saving image to {tmp_path}/output.png.")
        
        file = nextcord.File(f"{tmp_path}/output.png", filename="output.png")
        
        # Send image as response
        embed1 = load_embed()
        embed2 = {
            "image": {
                "url": "attachment://output.png"
            },
            "description": f"Prompt: `{prompt}`"
        }
        em = Embed().from_dict(embed1 | embed2)
        
        await interaction.channel.send(embed=em, file=file)
        logging.info("Sending repsonse message to channel.")
        
        # Cleanup
        await message.delete()
        try:
            for f in os.listdir(tmp_path):
                os.remove(os.path.join(tmp_path, f))
            logging.info("Removed temporary files.")
        except OSError as e:
            logging.exception(e)

# Add Cog to bot
def setup(bot):
    bot.add_cog(StableDiffusion(bot))
    logging.info("Stable Diffusion module loaded!")
