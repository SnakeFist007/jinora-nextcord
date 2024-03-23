# Jinora - Your Airbending Discord Bot!
<div align="center">
    <a href="https://www.python.org">
        <img src="https://custom-icon-badges.demolab.com/badge/Python-3.12.2-0F81C2?logo=python">
    </a>
    <a href="https://docs.nextcord.dev/en/stable/">
        <img src="https://custom-icon-badges.demolab.com/badge/Nextcord-2.6.1-5865F2?logo=nextcord">
    </a>
    <a href="https://www.mongodb.com">
        <img src="https://custom-icon-badges.demolab.com/badge/MongoDB-7.0-13AA52?logo=mongodb">
    </a>
    <a href="https://www.docker.com">
        <img src="https://custom-icon-badges.demolab.com/badge/Docker-26.0-2496ED?logo=docker">
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

<hr><br>

<p align="center">
This project is a personal journey to improve my Python skills and how to make a neat Discord-Bot!
</p>

<p align="center">
    <a href="https://github.com/SnakeFist007/jinora-nextcord/releases/latest">
        <img src="https://img.shields.io/badge/Bot%20Version-3.0.0-blue.svg?style=for-the-badge&logo=Python">
    </a>
</p>

<p align="center">
    If you like this project, please consider leaving a ⭐
</p>

<p align="center">
    <a href="#-features">Features</a>
  •
    <a href="#-installation">Installation</a>
  •
    <a href="#-legal-information">Legal Information</a>
</p>

---

# <img src="database/bot-logo.png" width=24px height=24px> Features
1. Weather & Astro Commands
2. Daily Weather & Astro Report
3. Daily Inspirational Quotes

<br>

# <img src="database/bot-logo.png" width=24px height=24px> Running the Bot
First download the [.env.example](/.env.example) template from the repository.


## Requirements

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
```

Then start the image with the variables from the .env file:
```
docker run --env-file .env -d <id>
```

<br>

# <img src="database/bot-logo.png" width=24px height=24px> Misc. Information

## License
This project is licensed under the [GNU Affero General Public License 3.0](/LICENSE).

## Semantic Versioning
I use [SemVer](https://semver.org) for versioning. For all available versions, see the [tags](https://github.com/SnakeFist007/jinora-nextcord/tags) from this repository.

## Resources
All images of Jinora have been generated with [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui), [Based65](https://civitai.com/models/31546/based65) and the amazing [Jinora LoRA](https://civitai.com/models/51783/jinora-the-legend-of-korra-lora), as well as being upscaled with `R-ESRGAN-4x+-Anime6B`.

This project is not affiliated with the creators of "The Legend of Korra" or the Avatar franchise!

---

```
© 2023-2024, made by SnakeFist007 with ❤️
>
> ────▓▓▓▓▓▓──────   
> ───▓▄▓▓▓▓▓▓─────          _
> ──────▓▓▓▓▓─▓───      __ (_) 
> ─▓▓▓▓▓▓▓▓▓──▓▓──      \ \ _ _ __   ___  _ __ __ _ 
> ▓▓▓▓▓──────▓▓▓▓─       \ \ | '_ \ / _ \| '__/ _` |
> ─▓▓▓▓▓───▓▓▓▓▓──    /\_/ / | | | | (_) | | | (_| |
> ──▓▓▓▓▓▓▓▓▓▓▓───    \___/|_|_| |_|\___/|_|  \__,_|
> ─────▓▓▓▓▓──────   
>
```