import json
from nextcord import Embed

# Load data from JSON
def parse_json(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    
    return data

# Load text data from JSON
def parse_json_utf8(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    return data
    
# Load embed from JSON and parse as nextcord.Embed()
def parse_embed(path):
    data = parse_json(path)
    embed = Embed().from_dict(data)
    
    return embed

# Default error message
def load_error_msg():
    with open("database/embeds/error_embed.json", "r") as json_file:
        error = json.load(json_file)
    em = Embed().from_dict(error)
        
    return em

# Insufficient perms
def load_perms_msg(): 
    return parse_embed("database/embeds/perms_embed.json")