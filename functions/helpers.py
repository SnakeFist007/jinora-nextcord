import json
from nextcord import Embed
from functions.paths import messages, errors, emote_urls


# * Pure Helpers
class JSONLoader():
    @staticmethod
    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data


class EmbedBuilder():
    # Default template with footer text & icon
    @staticmethod
    def bake(raw):
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
    def bake_thumbnail(raw):
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['sunny']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)
    
    # Template with question thumbnail
    @staticmethod
    def bake_questioning(raw):
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['questioning']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)

    # Template with laughing thumbnail
    @staticmethod
    def bake_joke(raw):
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
    def welcome():
        return EmbedBuilder.bake_thumbnail(JSONLoader.load(messages)["welcome"])
    

# * Prebuilt Errors
class ErrorHandler:
    @staticmethod
    def default():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_default"])

    @staticmethod
    def perms():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_permissions"])

    @staticmethod
    def dm():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_dm"])

    @staticmethod
    def guild():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_guild"])

    @staticmethod
    def cooldown(self):
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_cooldown"])