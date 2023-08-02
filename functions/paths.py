from pathlib import Path


# Base Path object
base_path = Path(".")

cogs = base_path / "cogs"
embeds = base_path / "database/embeds"
ascii_art = base_path / "database/ascii_art"

# /mystery
wisdom = base_path / "database/mystery/db_wisdom.json"
eight_ball = base_path / "database/mystery/db_8ball.json"
# /qotd
qotd = base_path / "database/questions/qotd.json"
# /weather
conditions = base_path / "database/weather/weather_conditions.json"
# /astro
moon_phases = base_path / "database/weather/moon_phases.json"