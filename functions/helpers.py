import json
from nextcord import Embed


EMBED_PATH = "database/embeds"

# Basic functions
# * Load data from JSON
def parse_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    
    return data

# * Load text data from JSON
def parse_json_utf8(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    return data


# * Fuse 2 JSON objects
def fuse_json(json1, json2):
    return json1 | json2



# Specialized for embeds
# * Load raw data from JSON w/ pointer
def parse_json_raw(path, pointer):
    raw = parse_json(path)
    return raw[pointer]
    
# * Convert raw JSON data to nextcord.Embed()
def convert_raw(raw):
    return Embed().from_dict(raw)


# Default embed options
# * Load embed defaults
def __embed_defaults():
    return parse_json_raw(f"{EMBED_PATH}/defaults.json", "default")

# * Load embed defaults w/ thumbnail
def __embed_defaults_thumbnail():
    return parse_json_raw(f"{EMBED_PATH}/defaults.json", "default_thumbnail")

def __embed_question_thumbnail():
    return parse_json_raw(f"{EMBED_PATH}/defaults.json", "question_thumbnail")

def __embed_laughing_thumbnail():
    return parse_json_raw(f"{EMBED_PATH}/defaults.json", "laughing_thumbnail")


# * RAW BUILDER
# Returns JSON object
def bake_raw(raw):
    return __embed_defaults() | raw

def bake_raw_thumbnail(raw):
    return __embed_defaults_thumbnail() | raw


# * EMBED BUILDER
# Returns nextcord.Embed() object
def bake_embed(raw):
    return Embed().from_dict(__embed_defaults() | raw)

def bake_embed_thumbnail(raw):
    return Embed().from_dict(__embed_defaults_thumbnail() | raw)


# * HYBRID BUILDER
# Returns nextcord.Embed() object
def create_embed(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(__embed_defaults() | raw)

def create_embed_thumbnail(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(__embed_defaults_thumbnail() | raw)



# * Pre-built raws
# ON_JOIN Welcome message
def em_welcome():
    return create_embed_thumbnail(f"{EMBED_PATH}/messages.json", "welcome")

# /8ball and /wisdom
def raw_mystery():
    return __embed_question_thumbnail()

# /joke
def raw_joke():
    return __embed_laughing_thumbnail()

# /generate message
def raw_generate():
    return parse_json_raw(f"{EMBED_PATH}/messages.json", "stablediffusion")


# * Pre-built embeds
# /help message
def em_help():
    return create_embed(f"{EMBED_PATH}/messages.json", "help")


# ERROR: Default message
def em_error():
    return create_embed(f"{EMBED_PATH}/errors.json", "error_default")

# ERROR: Insufficient perms
def em_error_perms():
    return create_embed(f"{EMBED_PATH}/errors.json", "error_permissions")

# ERROR: Stable Diffusion is offline
def em_error_offline():
    return create_embed(f"{EMBED_PATH}/errors.json", "error_offline")