import json
from nextcord import Embed
from functions.paths import defaults, messages, errors


# * Pure Helpers
class JSONLoader():
    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

class EmbedBuilder():
    def bake(raw):
        return Embed().from_dict(JSONLoader.load(defaults)["default"] | raw)

    def bake_thumbnail(raw):
        return Embed().from_dict(JSONLoader.load(defaults)["default_thumbnail"] | raw)

    def bake_questioning(raw):
        return Embed().from_dict(JSONLoader.load(defaults)["question_thumbnail"] | raw)

    def bake_joke(raw):
        return Embed().from_dict(JSONLoader.load(defaults)["laughing_thumbnail"] | raw )


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