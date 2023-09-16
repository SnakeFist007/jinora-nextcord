# Jinora - Your Airbending Mood Tracker!
<div align="center">
    <a href="https://www.python.org">
        <img src="https://custom-icon-badges.demolab.com/badge/Python-3.11.4-0F81C2?logo=python">
    </a>
    <a href="https://docs.nextcord.dev/en/stable/">
        <img src="https://custom-icon-badges.demolab.com/badge/Nextcord-2.5.0-5865F2?logo=nextcord">
    </a>
    <a href="https://www.mongodb.com">
        <img src="https://custom-icon-badges.demolab.com/badge/MongoDB-7.0-13AA52?logo=mongodb">
    </a>
    <a href="https://www.docker.com">
        <img src="https://custom-icon-badges.demolab.com/badge/Docker-4.21.1-2496ED?logo=docker">
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
        <img src="https://img.shields.io/badge/Bot%20Version-2.1.0-blue.svg?style=for-the-badge&logo=Python">
    </a>
    <a href="https://discord.gg/aJwqJtnyS4">
        <img src="https://img.shields.io/discord/1134861717185253478.svg?label=Discord&logo=Discord&colorB=007ec6&style=for-the-badge">
    </a>
</p>

<p align="center">
    <a href="#-about">About</a>
  •
    <a href="#-features">Features</a>
  •
    <a href="#-installation">Installation</a>
  •
    <a href="#-contributors">Contributors</a>
  •
    <a href="#-legal-information">Legal Information</a>
</p>

<hr>

# <img src="database/bot-logo.png" width=24px height=24px> About
This project is all about the journey of learning Python and how to make a neat Discord bot. My primary goal is to improve my coding skills, learning and adhering to best practices throughout the process.

If you have any tips on how to improve this code, please let me know!

I do plan on "truly" releasing this bot in the near future, as soon as I got the main features down and can provide the service 24/7.

<br>

# <img src="database/bot-logo.png" width=24px height=24px> Features
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

# <img src="database/bot-logo.png" width=24px height=24px> Installation
First download the [.env.example](/.env.example) template from the repository.

## Useful links
Bot related:
- [Invite-Link](https://discord.com/oauth2/authorize?client_id=723619199523487883&permissions=274877958144&scope=bot%20applications.commands)
- [Support-Server](https://discord.gg/aJwqJtnyS4)

Everything need for bot development:
- [Nextcord Documentation](https://docs.nextcord.dev/en/stable/index.html)
- [Embed Generator](https://embed.dan.onl)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html#0)


## Configuration

⚠️ **Note: Never commit or share any API keys or tokens publicly!** ⚠️

Rename `.env.example` to `.env` and fill in your data! You need:
1. [Discord Bot Token](https://discord.com/developers/applications)
2. [Papertrail URL & Port](https://www.papertrail.com)
3. [MongoDB URI](https://account.mongodb.com/account/login)
4. [Weather API](https://www.weatherapi.com)
5. [Quotes API](https://api-ninjas.com/)
6. [Timezone TZ identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


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

# <img src="database/bot-logo.png" width=24px height=24px> Contributors

Be the first to create a pull request!

<br>

# <img src="database/bot-logo.png" width=24px height=24px> Legal Information

### GDPR Disclaimer
> While fictional characters do not fall under the GDPR, I would like to mention that I do not distribute or sell any information that is collected. Any information that is collected will be used soley for debugging purposes or reporting abuse to Discord.

Should you have any concerns about this, either contact me directly or do not use the bot. Thank you!

### License
This project is licensed under the [GNU Affero General Public License 3.0](/LICENSE).

### Semantic Versioning
I use [SemVer](https://semver.org) for versioning. For all available versions, see the [tags](https://github.com/SnakeFist007/jinora-nextcord/tags) from this repository.

### Resources
All images of Jinora have been generated with [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui), [Based65](https://civitai.com/models/31546/based65) & [Jinora LoRA](https://civitai.com/models/51783/jinora-the-legend-of-korra-lora), as well as being upscaled with `R-ESRGAN-4x+-Anime6B`.

This project is not affiliated with the creators of 'The Legend of Korra' or the Avatar franchise!

---

> Made by SnakeFist007 with ❤️
