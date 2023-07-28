from pathlib import Path

# Base Path object
base_path = Path(".")

cogs = base_path / "cogs"
embeds = base_path / "database/embeds"

# /txt2image
tmp_path = base_path / "cogs/stablediffusion/tmp"
gen_settings = base_path / "database/stable_diffusion/gen_settings.json"
# /mystery
wisdom = base_path / "database/mystery/db_wisdom.json"
eight_ball = base_path / "database/mystery/db_8ball.json"
# /weather
conditions = base_path / "database/weather/weather_conditions.json"
# /astro
moon_phases = base_path / "database/weather/moon_phases.json"