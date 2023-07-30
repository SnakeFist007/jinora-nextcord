import nextcord

class HelpButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Support Server", style=nextcord.ButtonStyle.url, url="https://discord.gg/aJwqJtnyS4"))
        self.add_item(nextcord.ui.Button(label="GitHub Repo", style=nextcord.ButtonStyle.url, url="https://github.com/SnakeFist007/jinora-nextcord"))
        