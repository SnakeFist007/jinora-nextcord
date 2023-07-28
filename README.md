# Jinora - Your Airbending Meditation Guide!
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



# Running the bot
Rename `.env.example` to `.env` and fill in your data! You need:
1. [Discord Bot Token](https://discord.com/developers/applications)
2. [MongoDB URI](https://account.mongodb.com/account/login)
3. [Weather API](https://www.weatherapi.com)
4. [Timezone TZ identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Deploy using Docker
Deploy the Docker image using:
```
docker build -t <user>/jinora-bot .
```
Then start:
```
docker run <id>
```



# Features
- [ ] Create recurring events
- [x] Reminders over Webhook Implementation
- [ ] Question of the Day -> Meditation of the Day!
- [x] Joke, 8-Ball & Wisdom Commands
- [x] Weather & Astro Commands

## Possible Features
- Tips for lucid dreaming -> hosted on external website
- Tarot Cards

## Cancelled Features
- Stable Music Player (via [Wavelink](https://github.com/PythonistaGuild/Wavelink), [Mafic](https://github.com/ooliver1/mafic) & [Lavalink-Servers](https://github.com/DarrenOfficial/lavalink-list)) -> doesn't work properly!
- Localization (🇩🇪, 🇬🇧, 🇫🇷)

## To-Dos
- [ ] Add DM support for most commands, restrict those that can't be used outside guilds
- [ ] Limit reminders to Moderators (manage_message permissions only)
- [ ] Limit recurring reminder to 10
- [ ] Replace /feed delete & /feed admin delete with Dropdown Menu
- [ ] Fine-tuned Permissions (not just Administrator for the bot)

<br>

# GDPR Legal Disclaimer
> While fictional characters do not fall under the GDPR, I would like to mention that I do not distribute or sell any information that is collected. Any information that is collected will be used soley for debugging purposes or reporting abuse to Discord.

Should you have any concerns about this, either contact me directly or do not use the bot. Thank you!

<hr>

This project is licensed under the [GNU General Public License 3.0](/LICENSE).
