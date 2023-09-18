import nextcord
from nextcord import Interaction
from functions.helpers import ErrorHandler


async def default_error(interaction: Interaction) -> None:
    await interaction.send(embed=ErrorHandler.default())


async def dm_error(interaction: Interaction) -> None:
    try:
        await interaction.send(embed=ErrorHandler.dm())
    except nextcord.HTTPException:
        pass


async def perm_error(interaction: Interaction) -> None:
    await interaction.send(embed=ErrorHandler.perms())


async def guild_error(interaction: Interaction) -> None:
    await interaction.send(embed=ErrorHandler.guild())
    
    
async def cd_error(interaction: Interaction) -> None:
    await interaction.send(embed=ErrorHandler.cooldown())
