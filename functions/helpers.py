import json
import re
import random
from datetime import datetime, timedelta
from nextcord import Embed, File
from functions.paths import messages, errors


# * Misc Functions
def convert_day(day: str) -> int:
    key = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
           3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    return key[day]

def is_valid_time_format(input: str) -> bool:
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, input))

def daily_random(length: int) -> int:
    seed = datetime.now() - datetime(2000, 4, 23)

    random.seed(seed.days)
    return random.randint(1, length)

def get_weekday(desired_day, zone) -> int:
    next_day = (desired_day - datetime.now(zone).weekday()) % 7
    if next_day == 0:
        next_day = 7

    return datetime.now(zone) + timedelta(days=next_day)



# * Pure Helpers
class JSONLoader():
    @staticmethod
    def load(path) -> dict[str, str]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

class EmbedBuilder():
    # Default template with footer text & icon
    @staticmethod
    def bake(raw: dict[str, str]) -> Embed:
        output = {
            "color": 15844367
        }
        return Embed().from_dict(output | raw)

    # Default template with thumbnail
    @staticmethod
    def bake_thumbnail(raw: dict[str, str]) -> Embed:
        output = { 
            "thumbnail": { 
                "url": "attachment://image.png"
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)
    
    @staticmethod
    def get_emoji(path) -> File:
        return File(path, filename="image.png")



# * Prebuilt Embeds
class EmbedHandler:
    @staticmethod
    def welcome() -> Embed:
        return EmbedBuilder.bake_thumbnail(JSONLoader.load(messages)["welcome"])
    

# * Prebuilt Errors
class ErrorHandler:
    @staticmethod
    def default() -> Embed:
        return EmbedBuilder.bake(JSONLoader.load(errors)["default"])

    @staticmethod
    def perms() -> Embed:
        return EmbedBuilder.bake(JSONLoader.load(errors)["permissions"])

    @staticmethod
    def dm() -> Embed:
        return EmbedBuilder.bake(JSONLoader.load(errors)["dm"])

    @staticmethod
    def guild() -> Embed:
        return EmbedBuilder.bake(JSONLoader.load(errors)["guild"])

    @staticmethod
    def cooldown() -> Embed:
        return EmbedBuilder.bake(JSONLoader.load(errors)["cooldown"])