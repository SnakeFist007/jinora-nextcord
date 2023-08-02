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

# Emotes (imgur)
emote_urls = {
    "cloudy": "https://imgur.com/5zfRFq1.png",
    "greetings": "https://imgur.com/S3M5Kiu.png",
    "happy": "https://imgur.com/Nb5BMJs.png",
    "sipping": "https://imgur.com/2T4dqyL.png",
    "laughing": "https://imgur.com/oxP24J6.png",
    "meditating": "https://imgur.com/4vuMmhb.png",
    "neutral": "https://imgur.com/YmXLdWH.png",
    "night": "https://imgur.com/JF41h6h.png",
    "phone": "https://imgur.com/MuigdvJ.png",
    "proud": "https://imgur.com/a21jxMq.png",
    "questioning": "https://imgur.com/H9K383w.png",
    "rainy": "https://imgur.com/ZyW41zg.png",
    "reading": "https://imgur.com/fOZDtaA.png",
    "snowy": "https://imgur.com/Jq3Ci6T.png",
    "sunny": "https://imgur.com/HWQv848.png",
}