import json
from nextcord import Embed
from functions.paths import messages, errors, emote_urls


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
            "footer": {
                "text": "Jinora#2184"
            },
            "icon_url": f"{emote_urls['sunny']}",
            "color": 15844367
        }
        return Embed().from_dict(output | raw)

    # Default template with thumbnail
    @staticmethod
    def bake_thumbnail(raw: dict[str, str]) -> Embed:
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['sunny']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)
    
    # Template with question thumbnail
    @staticmethod
    def bake_questioning(raw: dict[str, str]) -> Embed:
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['questioning']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)

    # Template with laughing thumbnail
    @staticmethod
    def bake_joke(raw: dict[str, str]) -> Embed:
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['laughing']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)



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