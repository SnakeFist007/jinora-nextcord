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

    @nextcord.ui.button(label="Ja", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
        role_id = env.nsfw_role
        role = interaction.guild.get_role(role_id)
        assert isinstance(role, nextcord.Role)

        if role in interaction.user.roles:
            await interaction.response.send_message("Du hast bereits Zugriff auf die NSFW-Kanäle!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Zugriff auf die NSFW-Kanäle vergeben!", ephemeral=True)

    @nextcord.ui.button(label="Nein", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: Interaction):
        role_id = env.nsfw_role
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("Zugriff auf die NSFW-Kanäle entfernt!", ephemeral=True)
        else:
            await interaction.response.send_message("Du hast keinen Zugriff auf die NSFW-Kanäle!", ephemeral=True)

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
                                  description="Wift einen 3-seitigen Würfel."),
            nextcord.SelectOption(label="D6", emoji="🎲",
                                  description="Wift einen 6-seitigen Würfel."),
            nextcord.SelectOption(label="D12", emoji="🎲",
                                  description="Wift einen 12-seitigen Würfel."),
            nextcord.SelectOption(label="D20", emoji="🎲",
                                  description="Wift einen 20-seitigen Würfel."),
            nextcord.SelectOption(label="D100", emoji="🎲",
                                  description="Wift einen 100-seitigen Würfel.")
        ]
        super().__init__(placeholder="Würfel-Größe auswählen...",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "D3":
            await interaction.response.send_message(f"Eine `{random.randint(1,3)}` gewürfelt!", ephemeral=False)
        elif self.values[0] == "D6":
            await interaction.response.send_message(f"Eine `{random.randint(1,6)}` gewürfelt!", ephemeral=False)
        elif self.values[0] == "D12":
            await interaction.response.send_message(f"Eine`{random.randint(1,12)}` gewürfelt!", ephemeral=False)
        elif self.values[0] == "D20":
            await interaction.response.send_message(f"Eine `{random.randint(1,20)}` gewürfelt!", ephemeral=False)
        elif self.values[0] == "D100":
            await interaction.response.send_message(f"Eine `{random.randint(1,100)}` gewürfelt!", ephemeral=False)
        else:
            await interaction.response.send_message("Please select a valid option!", ephemeral=True)


class DiceDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DiceDropdown())


class GameAddDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Amogus", emoji="😏"),
            nextcord.SelectOption(label="DSA", emoji="🃏"),
            nextcord.SelectOption(label="Genshin Impact", emoji="💢"),
            nextcord.SelectOption(label="Minecraft", emoji="🧱"),
            nextcord.SelectOption(label="TTT", emoji="🔫")
        ]
        super().__init__(placeholder="Gewünschte Rollen auswählen...",
                         min_values=1, max_values=5, options=options)

    async def callback(self, interaction: Interaction):
        for role in self.values:
            if role == "Amogus":
                role_id = env.amogus_role
                add_role = interaction.guild.get_role(role_id)
                assert isinstance(add_role, nextcord.Role)

                await interaction.user.add_roles(add_role)

            if role == "DSA":
                role_id = env.dsa_role
                add_role = interaction.guild.get_role(role_id)
                assert isinstance(add_role, nextcord.Role)

                await interaction.user.add_roles(add_role)

            if role == "Genshin Impact":
                role_id = env.genshin_role
                add_role = interaction.guild.get_role(role_id)
                assert isinstance(add_role, nextcord.Role)

                await interaction.user.add_roles(add_role)

            if role == "Minecraft":
                role_id = env.minecraft_role
                add_role = interaction.guild.get_role(role_id)
                assert isinstance(add_role, nextcord.Role)

                await interaction.user.add_roles(add_role)

            if role == "TTT":
                role_id = env.ttt_role
                add_role = interaction.guild.get_role(role_id)
                assert isinstance(add_role, nextcord.Role)

                await interaction.user.add_roles(add_role)
            
        return await interaction.response.send_message("Gewünschte Rollen hinzugefügt!", ephemeral=True)


class GameAddDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GameAddDropdown())


class GameRemoveDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Amogus", emoji="😏"),
            nextcord.SelectOption(label="DSA", emoji="🃏"),
            nextcord.SelectOption(label="Genshin Impact", emoji="💢"),
            nextcord.SelectOption(label="Minecraft", emoji="🧱"),
            nextcord.SelectOption(label="TTT", emoji="🔫")
        ]
        super().__init__(placeholder="Zu entfernende Rollen auswählen...",
                         min_values=1, max_values=5, options=options)

    async def callback(self, interaction: Interaction):
        for role in self.values:
            if role == "Amogus":
                role_id = env.amogus_role
                add_role = interaction.guild.get_role(role_id)

                await interaction.user.remove_roles(add_role)

            if role == "DSA":
                role_id = env.dsa_role
                add_role = interaction.guild.get_role(role_id)

                await interaction.user.remove_roles(add_role)

            if role == "Genshin Impact":
                role_id = env.genshin_role
                add_role = interaction.guild.get_role(role_id)

                await interaction.user.remove_roles(add_role)

            if role == "Minecraft":
                role_id = env.minecraft_role
                add_role = interaction.guild.get_role(role_id)

                await interaction.user.remove_roles(add_role)

            if role == "TTT":
                role_id = env.ttt_role
                add_role = interaction.guild.get_role(role_id)

                await interaction.user.remove_roles(add_role)

        return await interaction.response.send_message("Gewünschte Rollen entfernt!", ephemeral=True)


class GameRemoveDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GameRemoveDropdown())


# Initialize Cog
class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="nsfwaccess", description="Zugriff auf die NSFW-Kanäle verwalten", guild_ids=[testServerID])
    async def role_nsfw(self, interaction: Interaction):
        await interaction.send("Zugriff auf die NSFW-Kanäle?", view=YesNoButtons(), ephemeral=True)

    @nextcord.slash_command(name="setgender", description="Eine Geschlechter-Rolle auswählen", guild_ids=[testServerID])
    async def role_setgender(self, interaction: Interaction):
        await interaction.send(view=GenderDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="removegender", description="Geschlechter-Rolle entfernen", guild_ids=[testServerID])
    async def role_removegender(self, interaction: Interaction):
        user_roles = interaction.user.roles

        if interaction.guild.get_role(env.male_role) in user_roles:
            await interaction.user.remove_roles(interaction.guild.get_role(env.male_role))
            await interaction.response.send_message("Geschlechts-Rolle entfernt!", ephemeral=True)

        elif interaction.guild.get_role(env.female_role) in user_roles:
            await interaction.user.remove_roles(interaction.guild.get_role(env.female_role))
            await interaction.response.send_message("Geschlechts-Rolle entfernt!", ephemeral=True)

        elif interaction.guild.get_role(env.other_role) in user_roles:
            await interaction.user.remove_roles(interaction.guild.get_role(env.other_role))
            await interaction.response.send_message("Geschlechts-Rolle entfernt!", ephemeral=True)

        else:
            await interaction.response.send_message("Noch keine Geschlechts-Rolle vorhanden!", ephemeral=True) 

    @nextcord.slash_command(name="setgameroles", description="Zugriff auf die Games-Kanäle erhalten", guild_ids=[testServerID])
    async def role_addgame(self, interaction: Interaction):
        await interaction.send(view=GameAddDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="removegameroles", description="Zugriff auf die Games-Kanäle entfernen", guild_ids=[testServerID])
    async def role_removegame(self, interaction: Interaction):
        await interaction.send(view=GameRemoveDropdownView(), ephemeral=True)

    @nextcord.slash_command(name="rolldie", description="Einen Würfel werfen", guild_ids=[testServerID])
    async def dice_roll(self, interaction: Interaction):
        await interaction.send(view=DiceDropdownView(), ephemeral=True)

# Add Cog to bot
def setup(bot):
    bot.add_cog(Roles(bot))
    print("roles.py cog loaded!")
