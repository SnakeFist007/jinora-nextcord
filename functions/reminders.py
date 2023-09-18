import asyncio
from datetime import datetime
from dateutil import tz
from discord_webhook import DiscordWebhook as Webhook
from functions.helpers import EmbedBuilder, get_weekday
from functions.logging import logging


# Reminder function for Feeds
async def set_reminder(task: dict, timezone) -> None:
    # Prepare message
    webhook = Webhook(url=task["webhook"], content=f"<@&{task['role_id']}>")
    embed = {
        "title": "Reminder!",
        "description": f"{task['message']}"
    }
    webhook.add_embed(EmbedBuilder.bake(embed))
    
    # Get next occurance
    zone = tz.gettz(timezone)
    now = datetime.now(zone)
    
    dt_time = datetime.strptime(task["time"], "%H:%M")
    next_date = get_weekday(task["day"], zone)
    
    # Start scheduled reminder
    next_reminder = next_date.replace(hour=dt_time.hour, minute=dt_time.minute, second=0)
    wait_time = (next_reminder - now).total_seconds()
    logging.info(f"Task {task['internal_id']}: Arming reminder timer for {wait_time} seconds...")
    
    # Wait until date, then send webhook
    await asyncio.sleep(wait_time)
    try:
        webhook.execute()
        logging.info(f"Reminder triggered: Sending embed through webhook: {task['webhook']}")
        # Set new reminder
        set_reminder(task, timezone)
    except Exception as e:
        logging.exception(e)
        return