from pathlib import Path


# * Base Path object & important subfolders
base_path = Path(".")
cogs = base_path / "cogs"
embeds = base_path / "database/embeds"

# * Main files
ascii_art = base_path / "database/ascii_art"
messages = embeds / "messages.json"
errors = embeds / "errors.json"

# Cog: Weather
conditions = base_path / "database/weather/weather_conditions.json"
moon_phases = base_path / "database/weather/moon_phases.json"


# * Icons
ICO_CLOUDY = base_path / "database/icons/cloudy.png"
ICO_GREETINGS = base_path / "database/icons/greetings.png"
ICO_HAPPY = base_path / "database/icons/happy.png"
ICO_SIPPING = base_path / "database/icons/hot_chocolate.png"
ICO_LAUGHING = base_path / "database/icons/laughing.png"
ICO_MEDITATING = base_path / "database/icons/meditating.png"
ICO_NEUTRAL = base_path / "database/icons/neutral.png"
ICO_NIGHT = base_path / "database/icons/night.png"
ICO_PHONE = base_path / "database/icons/phone.png"
ICO_PROUD = base_path / "database/icons/proud.png"
ICO_QUESTIONING = base_path / "database/icons/questioning.png"
ICO_RAINY = base_path / "database/icons/rainy.png"
ICO_READING = base_path / "database/icons/reading.png"
ICO_SNOWY = base_path / "database/icons/snowy.png"
ICO_SUNNY = base_path / "database/icons/sunny.png"

icons = {
    "cloudy": ICO_CLOUDY,
    "greetings": ICO_GREETINGS,
    "happy": ICO_HAPPY,
    "sipping": ICO_SIPPING,
    "laughing": ICO_LAUGHING,
    "meditating": ICO_MEDITATING,
    "neutral": ICO_NEUTRAL,
    "night": ICO_NIGHT,
    "phone": ICO_PHONE,
    "proud": ICO_PROUD,
    "questioning": ICO_QUESTIONING,
    "rainy": ICO_RAINY,
    "reading": ICO_READING,
    "snowy": ICO_SNOWY,
    "sunny": ICO_SUNNY
}


# * Discord Emoji
EMO_AIR = "<:air:1136372942712881324>"
EMO_AIRNOMAD = "<:air_nomad:1136373972246732891>"
EMO_LOTUS = "<:white_lotus:1136372955908149290>"

EMO_BOOST = "<a:boost:1088152045166542959>"
EMO_SPARKLES = "<a:sparkles:1088152065034965104>"
EMO_YES = "<a:jape:1088151992800641054>"
EMO_MEH = "<a:meh:1088152028162822194>"
EMO_NOU = "<a:nope:1088151978456129696>"