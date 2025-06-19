import os

import aio_pika
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


RABBITMQ_URL: str = os.environ.get("RABBITMQ_URL")


async def publish_user_login_event(email: str, full_name: str) -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({
                "event": "user_logged_in",
                "email": email,
                "full_name": full_name
            }).encode()),
            routing_key="user_events"
        )
