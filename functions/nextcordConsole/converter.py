import nextcord
from nextcord.utils import get
import re


class Converter:
    def __init__(self, client):
        self.client: nextcord.Client = client
        self.covert_mapping = {
            bool: self.bool_converter,
            nextcord.User: self.user_converter,
            int: self.int_converter,
            nextcord.Guild: self.guild_converter
        }

    def get_id_match(self, id):
        match = re.search(r"[0-9]{15,21}", id)
        return True if match else False

    def bool_converter(self, param: str):
        if param.lower() in ["y", "yes", "on", "true", "1"]:
            return True
        elif param.lower() in ["n", "no", "off", "false", "0"]:
            return False
        raise TypeError(f"Cannot convert {param} into Bool")

    def user_converter(self, param):
        if self.get_id_match(param):
            return self.client.get_user(int(param))
        else:
            for user in self.client.users:
                if user.name + "#" + user.discriminator == param:
                    return user
            else:
                raise TypeError(f"Cannot convert {param} to User")

    def int_converter(self, param):
        try:
            return int(param)
        except TypeError:
            raise TypeError(f"Cannot convert {param} to int")

    def guild_converter(self, param):
        if self.get_id_match(param):
            return self.client.get_guild(int(param))
        else:
            guild = get(self.client.guilds, name=param)
            if guild:
                return guild
            else:
                raise TypeError(f"Cannot convert {param} to Guild")

    def get_converter(self, type):
        try:
            return self.covert_mapping[type]
        except KeyError:
            raise TypeError(f"{type} can not be converted.\nAdd a conversion behavior using the add_converter method.")

    def add_converter(self, type_, func):
        self.covert_mapping.update({type_: func})