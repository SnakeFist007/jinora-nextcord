import json
from nextcord import Embed
from functions.paths import messages, errors, emote_urls


# * Pure Helpers
class JSONLoader():
    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data


class EmbedBuilder():
    # Default template with footer text & icon
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
    def bake_thumbnail(raw):
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['sunny']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)
    
    # Template with question thumbnail
    def bake_questioning(raw):
        output = { 
            "thumbnail": { 
                "url": f"{emote_urls['questioning']}" 
            },
            "color": 15844367 
        }
        return Embed().from_dict(output | raw)

    # Template with laughing thumbnail
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
    def welcome():
        return EmbedBuilder.bake_thumbnail(JSONLoader.load(messages)["welcome"])
    

# * Prebuilt Errors
class ErrorHandler:
    def default():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_default"])

    def perms():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_permissions"])

    def dm():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_dm"])

    def guild():
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_guild"])

    def cooldown(self):
        return EmbedBuilder.bake(JSONLoader.load(errors)["error_cooldown"])