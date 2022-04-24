import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import commands
from main import testServerID
import random
import env

class YesNoButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
        role_id = env.nsfw_role
        role = interaction.guild.get_role(role_id)
        assert isinstance(role, nextcord.Role)

        if role in interaction.user.roles:
            await interaction.response.send_message("Du hast bereits Zugriff auf die NSFW-Kanäle!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Zugriff auf die NSFW-Kanäle vergeben!", ephemeral=True)

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Keinen Zugriff auf die NSFW-Kanäle vergeben!", ephemeral=True)

class GenderDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Männlich", emoji="♂️"),
            nextcord.SelectOption(label="Weiblich", emoji="♀️"),
            nextcord.SelectOption(label="Divers", emoji="⚧")
        ]
        super().__init__(placeholder="Geschlecht auswählen...",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "Männlich":
            role_id = env.male_role
            role = interaction.guild.get_role(role_id)
            assert isinstance(role, nextcord.Role)

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Rolle '{self.values[0]}' hinzugefügt!", ephemeral=True)
        elif self.values[0] == "Weiblich":
            role_id = env.female_role
            role = interaction.guild.get_role(role_id)
            assert isinstance(role, nextcord.Role)

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Rolle '{self.values[0]}' hinzugefügt!", ephemeral=True)
        elif self.values[0] == "Divers":
            role_id = env.other_role
            role = interaction.guild.get_role(role_id)
            assert isinstance(role, nextcord.Role)

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Rolle '{self.values[0]}' hinzugefügt!", ephemeral=True)


class GenderDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GenderDropdown())


class DiceDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="D3", emoji="🎲",
                                  description="Rolls a 3-sided game die."),
            nextcord.SelectOption(label="D6", emoji="🎲",
                                  description="Rolls a 6-sided game die."),
            nextcord.SelectOption(label="D12", emoji="🎲",
                                  description="Rolls a 12-sided game die."),
            nextcord.SelectOption(label="D20", emoji="🎲",
                                  description="Rolls a 20-sided game die."),
            nextcord.SelectOption(label="D100", emoji="🎲",
                                  description="Rolls a 100-sided game die."),
        ]
        super().__init__(placeholder="Select the die size...",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "D3":
            await interaction.send(f"Rolled a `{random.randint(1,3)}`!", ephemeral=False)
        elif self.values[0] == "D6":
            await interaction.send(f"Rolled a `{random.randint(1,6)}`!", ephemeral=False)
        elif self.values[0] == "D12":
            await interaction.send(f"Rolled a `{random.randint(1,12)}`!", ephemeral=False)
        elif self.values[0] == "D20":
            await interaction.send(f"Rolled a `{random.randint(1,20)}`!", ephemeral=False)
        elif self.values[0] == "D100":
            await interaction.send(f"Rolled a `{random.randint(1,100)}`!", ephemeral=False)
        else:
            await interaction.response.send_message("Please select a valid option!", ephemeral=True)


class DiceDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DiceDropdown())

# Initialize Cog
class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="nsfwconfirm", description="Zugriff auf die NSFW-Kanäle erhalten", guild_ids=[testServerID])
    async def role_nsfwconfirm(self, interaction: Interaction):
        await interaction.send(view=YesNoButtons(), ephemeral=True)

    @nextcord.slash_command(name="setgender", description="Wähle ein Geschlecht aus", guild_ids=[testServerID])
    async def role_setgender(self, interaction: Interaction):
        await interaction.send(view=GenderDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="rolldie", description="Roll a die.", guild_ids=[testServerID])
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)

# Add Cog to bot
def setup(bot):
    bot.add_cog(Roles(bot))
    print("roles.py cog loaded!")
