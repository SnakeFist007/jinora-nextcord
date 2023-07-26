import json
from nextcord import Embed


embed_path = "database/embeds"

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
def covert_raw(raw):
    return Embed().from_dict(raw)


# Default embed options
# * Load embed defaults
def embed_defaults():
    return parse_json_raw(f"{embed_path}/defaults.json", "default")

# * Load embed defaults w/ thumbnail
def embed_defaults_thumbnail():
    return parse_json_raw(f"{embed_path}/defaults.json", "default_thumbnail")


# ! EXTERNAL USE ONLY!
# Returns JSON object
def bake_raw(raw):
    return embed_defaults() | raw

def bake_raw_thumbnail(raw):
    return embed_defaults_thumbnail() | raw

# Returns nextcord.Embed() object
def bake_embed(raw):
    return Embed().from_dict(embed_defaults() | raw)

def bake_embed_thumbnail(raw):
    return Embed().from_dict(embed_defaults_thumbnail() | raw)


# ! INTERNAL USE ONLY!
# Returns nextcord.Embed() object
def create_embed(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(embed_defaults() | raw)

def create_embed_thumbnail(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(embed_defaults_thumbnail() | raw)


# Pre-built embeds
# * ON_JOIN Welcome message
def em_welcome():
    return create_embed_thumbnail(f"{embed_path}/messages.json", "welcome")

# * /help message
def em_help():
    return create_embed(f"{embed_path}/messages.json", "help")

# * /generate message
def raw_generate():
    return parse_json_raw(f"{embed_path}/messages.json", "stablediffusion")

# * ERROR: Default message
def em_error():
    return create_embed(f"{embed_path}/errors.json", "error_default")

# * ERROR: Insufficient perms
def em_error_perms():
    return create_embed(f"{embed_path}/errors.json", "error_permissions")

def em_error_offline():
    return create_embed(f"{embed_path}/errors.json", "error_offline")