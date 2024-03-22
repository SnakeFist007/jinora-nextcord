import os
import asyncio
import nextcord.utils
from dotenv import load_dotenv
from datetime import datetime
from dateutil import tz
from functions.apis import get_quote
from functions.helpers import EmbedBuilder
from functions.logging import logging
from functions.bot import bot


load_dotenv()
TIMEZONE = os.getenv("TIMEZONE")

client = nextcord.Client()
timezone = tz.gettz(TIMEZONE)


# Get next occurance
def get_waittime(task):
    now = datetime.now(timezone)
    input_time = datetime.strptime(task["time"], "%H:%M")
    date = input_time.replace(
        year=now.year, month=now.month, day=now.day, second=0).replace(tzinfo=timezone)

    if now > date:
        date = date.replace(day=(now.day + 1))

    # Start scheduled reminder
    return (date - now).total_seconds()


# Universal task handler
async def set_task(task: dict) -> None:
    # Prepare message
    try:
        data = await get_quote()
            
    except Exception as e:
        logging.exception(e)
                    
    embed = { "title": f"{data[0]['quote']} *~{data[0]['author']}*" }
        
    em = EmbedBuilder.bake(embed)

    wait_time = get_waittime(task)
    logging.info(f"Task {task['internal_id']}: Arming task, ready in {wait_time} seconds...")

    # Wait until date, then send message
    await asyncio.sleep(wait_time)
    
    channel = bot.get_channel(task["channel_id"])
    try:
        await channel.send(embed=em)

    except Exception as e:
        logging.exception(e)
        return
    
    # Reset task scheduler
    await set_task(task)
    
    
async def stop_task(internal_id: str) -> None:
    try:
        for task in asyncio.all_tasks():
            if task.get_name() == internal_id:
                logging.warning(f"Stopped task {internal_id}!")
                task.cancel()
        
    except Exception as e:
        logging.exception(e)
