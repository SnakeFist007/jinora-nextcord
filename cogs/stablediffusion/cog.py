import nextcord
import requests
import io
import base64
import os
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands, application_checks
from typing import Optional
from PIL import Image
from main import logging, url, parse_json, em_error, em_error_offline, fuse_json, raw_generate, bake_embed


tmp_path = "cogs/stablediffusion/tmp"

# Create tmp directory for generated Stable Diffusion images
def prepare_directory():
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
        logging.warning(
            "Temporary image directory missing! Creating a new one...")

# Loads default values for image generation
def load_defaults():
    defaults = parse_json("database/stable_diffusion/bot_settings.json")
    return defaults


# Initialize Cog
class StableDiffusion(commands.Cog, name="StableDiffusion"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # * Generate command
    @nextcord.slash_command(name="generate", description="Generates a picture! (txt2img)")
    async def sd_generate(
            self, interaction: Interaction,
            prompt: str = SlashOption(description="Insert your prompt"),
            negative_prompt: Optional[str] = SlashOption(description="Insert your negative prompt", required=False, default="")):

        # Put command message on hold
        await interaction.response.defer()
        logging.info("Recieving Stable Diffusion txt2img instruction...")
        message = await interaction.channel.fetch_message(int(interaction.channel.last_message_id))

        prepare_directory()

        # Assemble payload for Stable Diffusion
        defaults = load_defaults()
        user_input = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        prt_payload = defaults | user_input

        # Send request to Stable Diffusion API
        try:
            logging.info(f"Sending prompt payload to {url}.")
            res = requests.post(
                url=f"{url}/sdapi/v1/txt2img", json=prt_payload)

        except requests.exceptions.RequestException:
            logging.exception("Stable Diffusion Server is offline!")
            await interaction.channel.send(embed=em_error_offline())

        except Exception as e:
            logging.exception(e)
            await interaction.channel.send(embed=em_error())

        # Extract image and prepare for Discord
        try:
            r = res.json()
            for i in r["images"]:
                image = Image.open(io.BytesIO(
                    base64.b64decode(i.split(",", 1)[0])))
                image.save(f"{tmp_path}/output.png")
                logging.info(f"Saving image to {tmp_path}/output.png.")

            file = nextcord.File(
                f"{tmp_path}/output.png", filename="output.png")

            # Send image as response
            embed = {
                "image": {
                    "url": "attachment://output.png"
                },
                "description": f"Prompt: `{prompt}`"
            }
            em = bake_embed(fuse_json(raw_generate(), embed))

            await interaction.channel.send(embed=em, file=file)
            logging.info("Sending repsonse message to channel.")

        except (nextcord.errors.ApplicationInvokeError, UnboundLocalError):
            logging.exception("Command failed due to Stable Diffusion being offline.")

        except Exception as e:
            logging.exception(e)

        # Cleanup
        finally:
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
