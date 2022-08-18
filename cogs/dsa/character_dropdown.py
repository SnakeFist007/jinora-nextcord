import random
import nextcord
from nextcord import Interaction


# TODO: Dropdown-Menu with a list of all saved characters
class DelCharDropdown(nextcord.ui.Select):
    ...


class DelCharDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DelCharDropdown())
        
        
# TODO: Dropdown-Menu with a list of all saved characters
# TODO: Send saved JSON-file as attachment in reply
class DownloadCharDropdown(nextcord.ui.Select):
    ...


class DownloadCharDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DownloadCharDropdown())