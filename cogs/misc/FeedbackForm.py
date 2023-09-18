import nextcord
from nextcord import Interaction
from functions.helpers import EmbedBuilder
from functions.paths import questioning, laughing
from main import FEEDBACK_ID


class FeedbackForm(nextcord.ui.Modal):
    def __init__(self, bot) -> None:
        super().__init__(title="Feedback Form")
        self.bot = bot

        self.mTitle = nextcord.ui.TextInput(
            label="Title", min_length=2, max_length=128, required=True)
        self.add_item(self.mTitle)

        self.mBody = nextcord.ui.TextInput(
            label="Your Feedback", min_length=2, max_length=2000, required=True, style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.mBody)

    async def callback(self, interaction: Interaction) -> None:
        channel = self.bot.get_channel(FEEDBACK_ID)
        title = self.mTitle.value
        body = self.mBody.value

        fb_raw = {
            "title": title,
            "description": body
        }
        fb_em = EmbedBuilder.bake_questioning(fb_raw)

        res_raw = {
            "title": "Feedback sent successfully!",
            "description": "Thank you for your input!"
        }
        res_em = EmbedBuilder.bake_thumbnail(res_raw)

        # Send feedback to support server channel & give confirmation to user
        await channel.send(file=EmbedBuilder.get_emoji(questioning), embed=fb_em)
        return await interaction.response.send_message(file=EmbedBuilder.get_emoji(laughing), embed=res_em, ephemeral=True)
