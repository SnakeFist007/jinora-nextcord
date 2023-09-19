import os
import asyncio
import nextcord.utils
from dotenv import load_dotenv
from nextcord import ChannelType
from discord_webhook import DiscordWebhook as Webhook
from datetime import datetime, timedelta
from dateutil import tz
from functions.apis import get_quote, get_question
from functions.helpers import EmbedBuilder, get_weekday
from functions.logging import logging
from functions.paths import reading, questioning
from functions.bot import bot


load_dotenv()
TIMEZONE = os.getenv("TIMEZONE")

client = nextcord.Client()
timezone = tz.gettz(TIMEZONE)

# Reminder function for QotD
async def set_daily(daily: dict) -> None:
    # Prepare message
    if daily["mode"] == "quote":
        try:
            data = await get_quote()
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*",
                "description": "Sometimes quotes can be very insightful... Other times, not so much."
            }
            file = EmbedBuilder.get_emoji(reading)
            em = EmbedBuilder.bake_thumbnail(embed)

        except Exception as e:
            logging.exception(e)

    elif daily["mode"] == "question":
        try:
            output = get_question()
            embed = {
                "title": f"{output}",
                "description": "Need something to reflect on? I've got you covered!"
            }
            file = EmbedBuilder.get_emoji(questioning)
            em = EmbedBuilder.bake_thumbnail(embed)

        except Exception as e:
            logging.exception(e)

    # Get next occurance
    now = datetime.now(timezone)
    input_time = datetime.strptime(daily["time"], "%H:%M")
    date = input_time.replace(year=now.year, month=now.month, day=now.day, second=0).replace(tzinfo=timezone)
    
    if now > date:
        date = date.replace(day=(now.day + 1))

    # Start scheduled reminder
    wait_time = (date - now).total_seconds()
    logging.info(f"Daily {daily['internal_id']}: Arming reminder timer for {wait_time} seconds...")

    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)

    try:
        channel = bot.get_channel(daily["channel_id"])
        
        if daily["role_id"] != "None":
            
            if daily['threading'] != "False":
                message = await channel.send(file=file, embed=em)
                thread = await message.create_thread(name="Hi")
                await thread.send(f"<@&{daily['role_id']}>")
            
            else:
                await channel.send(content=f"<@&{daily['role_id']}>", file=file, embed=em)
        
        else:
            message = await channel.send(file=file, embed=em)
            
            if daily["threading"] != False:
                await message.create_thread(name=f"{daily['mode'].capitalize()} of the day!")

        # Set new daily
        await set_daily(daily)

    except Exception as e:
        logging.exception(e)
        return


# Reminder function for Feeds
async def set_reminder(task: dict) -> None:
    # Prepare message
    webhook = Webhook(url=task["webhook"], content=f"<@&{task['role_id']}>")
    embed = {
        "title": "Reminder!",
        "description": f"{task['message']}"
    }
    webhook.add_embed(EmbedBuilder.bake(embed))

    # Get next occurance
    input_time = datetime.strptime(task["time"], "%H:%M")
    now = datetime.now(timezone)
    next_date = get_weekday(task["day"], timezone)

    # Start scheduled reminder
    next_reminder = next_date.replace(
        hour=input_time.hour, minute=input_time.minute, second=0)
    wait_time = (next_reminder - now).total_seconds()
    logging.info(
        f"Task {task['internal_id']}: Arming reminder timer for {wait_time} seconds...")

    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)
    try:
        webhook.execute()
        logging.info(f"Reminder triggered: Sending embed through webhook: {task['webhook']}")
        # Set new reminder
        await set_reminder(task)
    except Exception as e:
        logging.exception(e)
        return
