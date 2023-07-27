# Jinora - Yet Another Discord Bot!
![](https://img.shields.io/badge/Python-3.11.4-0f81c2?logo=Python)
![](https://custom-icon-badges.herokuapp.com/badge/Nextcord-2.5.0-5865F2?logo=nextcord)
![](https://img.shields.io/badge/MongoDB-7.0-13aa52?logo=MongoDB)
![](https://img.shields.io/badge/Docker-4.21.1-2496ed?logo=Docker)

<img src="./database/bot-avatar-rounded.png" width="250" height="250">

**+++ Slash Commands ONLY! +++**

# Useful links
Everything need for bot development:
- [Invite-Link](https://discord.com/api/oauth2/authorize?client_id=723619199523487883&permissions=274877958144&scope=bot%20applications.commands)
- [Nextcord Documentation](https://docs.nextcord.dev/en/stable/index.html)
- [Embed Generator](https://embed.dan.onl)

<details>

<hr>

<summary> <b>Nextcord Color-Table</b> </summary>

Colors currently implemented with a name - converted to their int value:

| Name                | Int Value | Hex Code  |
| ------------------- | :-------: | :-------: |
| `Black`             |  2303786  | `#23272A` |
| `Blue`              |  3447003  | `#3498DB` |
| `Blurple`           |  5793266  | `#5865F2` |
| `DarkAqua`          |  1146986  | `#11806A` |
| `DarkBlue`          |  2123412  | `#206694` |
| `DarkButNotBlack`   |  2895667  | `#2C2F33` |
| `DarkGold`          | 12745742  | `#C27C0E` |
| `DarkGreen`         |  2067276  | `#1F8B4C` |
| `DarkGrey`          |  9936031  | `#979C9F` |
| `DarkNavy`          |  2899536  | `#2C3E50` |
| `DarkOrange`        | 11027200  | `#A84300` |
| `DarkPurple`        |  7419530  | `#71368A` |
| `DarkRed`           | 10038562  | `#992D22` |
| `DarkerGrey`        |  8359053  | `#7F8C8D` |
| `Default`           |     0     | `#000000` |
| `Fuchsia`           | 15418782  | `#EB459E` |
| `Gold`              | 15844367  | `#F1C40F` |
| `Green`             |  5763719  | `#57F287` |
| `Grey`              |  9807270  | `#95A5A6` |
| `Greyple`           | 10070709  | `#99AAb5` |
| `LuminousVividPink` | 15277667  | `#E91E63` |
| `Navy`              |  3426654  | `#34495E` |
| `Red`               | 15548997  | `#ED4245` |
| `White`             | 16777215  | `#FFFFFF` |
| `Yellow`            | 16776960  | `#FFFF00` |
[Source](https://gist.githubusercontent.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812/raw/fd8d2d0007a1c642c790bc308f27a2f2ca5c47c7/code_colors_discordjs.md)

</details>

<br>


# Running the bot

Rename `.env.example` to `.env` and fill in your data! You need:
1. [Discord Bot Token](https://discord.com/developers/applications)
2. [MongoDB URI](https://account.mongodb.com/account/login)
3. [Stable Diffusion API URL](http://127.0.0.1:7860)
4. [Weather API](https://www.weatherapi.com)
5. [Timezone TZ identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Method 1: Use Docker
Deploy the Docker image using:
```
docker build -t <user>/jinora-bot .
```
Then start:
```
docker run <id>
```

## Method 2: Run directly
Alternatively, **while _not_ recommended**, you can run it without Docker.

First install all needed modules:
```
pip install -r requirements
```

Then start the bot:
```
python main.py
```

# Features
- [x] Deployable via Docker
- [x] Reminders over Webhook Implementation
- [x] Integrated Stable Diffusion API (local servers only)
- [x] Joke, 8-Ball & Wisdom Commands
- [x] Weather & Astro Command

## Possible Features
- Meme Command
- Moderation Commands
- Localization (🇩🇪, 🇬🇧, 🇫🇷)

## Cancelled Features
- Stable Music Player (via [Wavelink](https://github.com/PythonistaGuild/Wavelink), [Mafic](https://github.com/ooliver1/mafic) & [Lavalink-Servers](https://github.com/DarrenOfficial/lavalink-list)) -> doesn't work properly!

## To-Dos
- [ ] Fine-tuned Permissions (not just Administrator for the bot)

<br>

# GDPR Legal Disclaimer
> While fictional characters do not fall under the GDPR, I would like to mention that I do not distribute or sell any information that is collected. Any information that is collected will be used soley for debugging purposes or reporting abuse to Discord.

Should you have any concerns about this, either contact me directly or do not use the bot. Thank you!

<hr>

This project is licensed under the [GNU General Public License 3.0](/LICENSE).