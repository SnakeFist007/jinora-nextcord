import json
from nextcord import Embed

def parse_embed(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    
    embed = Embed().from_dict(data)
    return embed