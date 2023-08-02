from pathlib import Path


# * Base Path object
base_path = Path(".")


# * Subfolders
cogs = base_path / "cogs"
embeds = base_path / "database/embeds"


# * Files
# Main
ascii_art = base_path / "database/ascii_art"

# Functions: Helpers
defaults = embeds / "defaults.json"
messages = embeds / "messages.json"
errors = embeds / "errors.json"

# Cog: Misc
wisdom = base_path / "database/mystery/db_wisdom.json"
eight_ball = base_path / "database/mystery/db_8ball.json"

# Cog: QotD
qotd = base_path / "database/questions/qotd.json"

# Cog: Weather
conditions = base_path / "database/weather/weather_conditions.json"
moon_phases = base_path / "database/weather/moon_phases.json"