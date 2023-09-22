import os
import asyncio
import nextcord.utils
from dotenv import load_dotenv
from datetime import datetime
from dateutil import tz
from functions.apis import get_quote, get_question, get_mood
from functions.helpers import EmbedBuilder
from functions.logging import logging
from functions.paths import reading, questioning, laughing, scale, AIR_NOMAD
from functions.bot import bot


load_dotenv()
TIMEZONE = os.getenv("TIMEZONE")

client = nextcord.Client()
timezone = tz.gettz(TIMEZONE)

# Universal task handler
async def set_task(task: dict) -> None:
    # Prepare message
    if task["type"] == "qotd": 
        if task["mode"] == "quote":
            try:
                data = await get_quote()
            
            except Exception as e:
                logging.exception(e)
                    
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*"
            }

            thread_name = "Quote"

        elif task["mode"] == "question":
            output = get_question(task["lang"])
            embed = {
                "title": f"{output}"
            }
        
        thread_name = f"{task['mode'].capitalize()} of the day!"
    
    elif task["type"] == "mood":
        title = get_mood(task['lang'])
        
        embed = {
            "title": f"{AIR_NOMAD} {title}"
        }
        
        thread_name = f"{title}"
        
    em = EmbedBuilder.bake(embed)

    # Get next occurance
    now = datetime.now(timezone)
    input_time = datetime.strptime(task["time"], "%H:%M")
    date = input_time.replace(
        year=now.year, month=now.month, day=now.day, second=0).replace(tzinfo=timezone)

    if now > date:
        date = date.replace(day=(now.day + 1))

    # Start scheduled reminder
    wait_time = (date - now).total_seconds()
    logging.info(f"Task {task['internal_id']}: Arming task, ready in {wait_time} seconds...")

    # Wait until date, then send message
    await asyncio.sleep(wait_time)
    
    channel = bot.get_channel(task["channel_id"])
    try:
        if task["role_id"] != "None":
            
            if task['threading'] == True:
                message = await channel.send(embed=em)
                thread = await message.create_thread(name=thread_name)
                await thread.send(f"<@&{task['role_id']}>")

            elif task['threading'] == False:
                message = await channel.send(content=f"<@&{task['role_id']}>", embed=em)


        elif task["role_id"] == "None":
            
            if task["threading"] == True:
                message = await channel.send(embed=em)
                await message.create_thread(name=thread_name)
            
            elif task['threading'] == False:
                message = await channel.send(embed=em)
             
                
        if task["type"] == "mood":
            for item in scale:
                await message.add_reaction(item)

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
