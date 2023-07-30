# Jinora - Your Airbending Meditation Guide!
<div align="center">
    <a href="https://www.python.org">
        <img src="https://custom-icon-badges.herokuapp.com/badge/Python-3.11.4-0F81C2?logo=python">
    </a>
    <a href="https://docs.nextcord.dev/en/stable/">
        <img src="https://custom-icon-badges.herokuapp.com/badge/Nextcord-2.5.0-5865F2?logo=nextcord">
    </a>
    <a href="https://www.mongodb.com">
        <img src="https://custom-icon-badges.herokuapp.com/badge/MongoDB-7.0-13AA52?logo=mongodb">
    </a>
    <a href="https://www.docker.com">
        <img src="https://custom-icon-badges.herokuapp.com/badge/Docker-4.21.1-2496ED?logo=docker">
    </a>
    <a href="https://www.codefactor.io/repository/github/snakefist007/jinora-nextcord">
        <img src="https://www.codefactor.io/repository/github/snakefist007/jinora-nextcord/badge">
    </a>
</div>

<br>

<div align="center">
    <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
        <img src="./database/bot-banner.png" width=75% height=75%>
    </a>
</div>

<hr>

<p align="center">
    If you like this project, please consider leaving a ⭐ for the repo!
</p>

<p align="center">
    <a href="https://github.com/SnakeFist007/jinora-nextcord/releases/latest">
        <img src="https://img.shields.io/badge/Bot%20Version-1.1.1-blue.svg?style=for-the-badge&logo=Python">
    </a>
    <a href="https://discord.gg/aJwqJtnyS4">
        <img src="https://img.shields.io/discord/1134861717185253478.svg?label=Discord&logo=Discord&colorB=007ec6&style=for-the-badge">
    </a>
</p>

<p align="center">
  <a href="#-features">Features</a>
  •
  <a href="#-useful-links">Useful Links</a>
  •
  <a href="#-running-the-bot">Running the bot</a>
  •
  <a href="#-contributors">Contributors</a>
  •
  <a href="#%EF%B8%8F-legal-information">Legal Information</a>
</p>

<hr>

# ✨ Features
- Question of the Day
- Random Wisdoms & Quotes
- Weather & Astro Commands
- Reminders over Webhook Implementation
- Joke & 8-Ball Commands


## Roadmap
See the [open issues](https://github.com/SnakeFist007/jinora-nextcord/issues) for a list of planned features and known issues.


## Contributing
Want to improve this project yourself? Any contributions you make are greatly appreciated!
- [Contributions Guide](/.github/CONTRIBUTIONS.md)
- [Translations Guide](/.github/TRANSLATIONS.md)

<br>

# 🔗 Useful links
Bot related:
- [Invite-Link](https://discord.com/oauth2/authorize?client_id=723619199523487883&permissions=274877958144&scope=bot%20applications.commands)
- [Support-Server](https://discord.gg/aJwqJtnyS4)

Everything need for bot development:
- [Nextcord Documentation](https://docs.nextcord.dev/en/stable/index.html)
- [Embed Generator](https://embed.dan.onl)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html#0)

<br>

# 🛠 Running the bot
First download the [.env.example](/.env.example) template from the repository.

## Configuration

⚠️ **Note: Never commit or share any API keys or tokens publicly!** ⚠️

Rename `.env.example` to `.env` and fill in your data! You need:
1. [Discord Bot Token](https://discord.com/developers/applications)
2. [MongoDB URI](https://account.mongodb.com/account/login)
3. [Weather API](https://www.weatherapi.com)
4. [Quotes API](https://api-ninjas.com/)
5. [Timezone TZ identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


## Deploy using Docker
Deploy & prepare the Docker image using:
```
docker pull ghcr.io/snakefist007/jinora-nextcord:latest
docker cp .env <container_id>:/.env
```
This will create the .env file with your token and keys inside the container.

Then start the image:
```
docker run <id>
```

**The bot should be running now!**

<br>

# 🤝 Contributors

## Translations
Be the first to create a pull request!

<br>

# ⚖️ Legal Information

### GDPR Disclaimer
> While fictional characters do not fall under the GDPR, I would like to mention that I do not distribute or sell any information that is collected. Any information that is collected will be used soley for debugging purposes or reporting abuse to Discord.

Should you have any concerns about this, either contact me directly or do not use the bot. Thank you!

### License
This project is licensed under the [GNU Affero General Public License 3.0](/LICENSE).

---

> Made by SnakeFist007 with ❤️
