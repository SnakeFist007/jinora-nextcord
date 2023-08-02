import json
from nextcord import Embed
from functions.paths import defaults, messages, errors


# Basic functions
# * Load data from JSON
def parse_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    
    return data

# * Load text data from JSON
def parse_json_utf8(path):
    with open(path, "r", encoding="utf-8") as f:
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
    return parse_json_raw(defaults, "default")

# * Load embed defaults w/ thumbnail
def __embed_defaults_thumbnail():
    return parse_json_raw(defaults, "default_thumbnail")

def __embed_question_thumbnail():
    return parse_json_raw(defaults, "question_thumbnail")

def __embed_laughing_thumbnail():
    return parse_json_raw(defaults, "laughing_thumbnail")


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

def bake_embed_questioning(raw):
    return Embed().from_dict(__embed_question_thumbnail() | raw)


# * HYBRID BUILDER
# Returns nextcord.Embed() object
def create_embed(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(__embed_defaults() | raw)

def create_embed_thumbnail(path, pointer):
    raw = parse_json_raw(path, pointer)
    return Embed().from_dict(__embed_defaults_thumbnail() | raw)



# * Pre-built raws
# /8ball and /wisdom
def raw_mystery():
    return __embed_question_thumbnail()

# /joke
def raw_joke():
    return __embed_laughing_thumbnail()


# * Pre-built embeds
# ON_JOIN Welcome message
def em_welcome():
    return create_embed_thumbnail(messages, "welcome")



# * ERRORS
# ERROR: Default message
def em_error():
    return create_embed(errors, "error_default")

# ERROR: Insufficient perms
def em_error_perms():
    return create_embed(errors, "error_permissions")

# ERROR: Command in DMs not available
def em_error_dm():
    return create_embed(errors, "error_dm")