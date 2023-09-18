import asyncio
from nextcord.ext import commands
from datetime import datetime, timedelta
from dateutil import tz
from functions.apis import get_quote, get_question
from functions.helpers import EmbedBuilder
from functions.logging import logging
from functions.paths import reading, questioning

bot = commands.Bot()

# Reminder function for QotD
async def set_daily(task: dict, timezone) -> None:
    # Prepare message
    channel = bot.get_channel(task["channel"])
    
    if task["mode"] == "quote":
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

    elif task["mode"] == "question":
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
    zone = tz.gettz(timezone)
    now = datetime.now(zone)
    
    dt_time = datetime.strptime(task["time"], "%H:%M")
    
    date = now + timedelta(days=1)
    next_day = date.replace(hour=dt_time.hour, minute=dt_time.minute, second=0)

    # Start scheduled reminder
    wait_time = (next_day - now).total_seconds()
    logging.info(f"Daily {task['internal_id']}: Arming reminder timer for {wait_time} seconds...")

    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)
    
    try:
        if task['role_id'] is not None:
            await channel.send(content=f"<@&{task['role_id']}>", file=file, embed=em)
            set_daily(task, timezone)
        else:
            await channel.send(file=file, embed=em)
            set_daily(task, timezone)
    
    except Exception as e:
        logging.exception(e)
        return
