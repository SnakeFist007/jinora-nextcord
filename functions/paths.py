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

# Emotes
cloudy = base_path / "database/emotes/cloudy.png"
greetings = base_path / "database/emotes/greetings.png"
happy = base_path / "database/emotes/happy.png"
sipping = base_path / "database/emotes/hot_chocolate.png"
laughing = base_path / "database/emotes/laughing.png"
meditating = base_path / "database/emotes/meditating.png"
neutral = base_path / "database/emotes/neutral.png"
night = base_path / "database/emotes/night.png"
phone = base_path / "database/emotes/phone.png"
proud = base_path / "database/emotes/proud.png"
questioning = base_path / "database/emotes/questioning.png"
rainy = base_path / "database/emotes/rainy.png"
reading = base_path / "database/emotes/reading.png"
snowy = base_path / "database/emotes/snowy.png"
sunny = base_path / "database/emotes/sunny.png"