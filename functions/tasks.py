import os
import asyncio
from dotenv import load_dotenv
from nextcord.ext import commands
from discord_webhook import DiscordWebhook as Webhook
from datetime import datetime, timedelta
from dateutil import tz
from functions.apis import get_quote, get_question
from functions.helpers import EmbedBuilder, get_weekday
from functions.logging import logging
from functions.paths import reading, questioning


load_dotenv()
TIMEZONE = os.getenv("TIMEZONE")

bot = commands.Bot()
timezone = tz.gettz(TIMEZONE)
now = datetime.now(timezone)

# Reminder function for QotD
async def set_daily(daily: dict) -> None:
    # Prepare message
    channel = bot.get_channel(daily["channel"])

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
    input_time = datetime.strptime(daily["time"], "%H:%M")
    
    if now > (now.replace(hour=input_time.hour, minute=input_time.minute)):
        date = now + timedelta(days=1)
    else:
        date = now
    
    next_day = date.replace(hour=input_time.hour,
                            minute=input_time.minute,
                            second=0)

    # Start scheduled reminder
    wait_time = (next_day - now).total_seconds()
    logging.info(f"Daily {daily['internal_id']}: Arming reminder timer for {wait_time} seconds...")

    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)

    try:
        if daily['role_id'] is not None:
            await channel.send(content=f"<@&{daily['role_id']}>", file=file, embed=em)          
        else:
            await channel.send(file=file, embed=em)

        # Set new daily
        set_daily(daily)

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
        set_reminder(task)
    except Exception as e:
        logging.exception(e)
        return
