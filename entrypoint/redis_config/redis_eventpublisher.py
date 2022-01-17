import json
import redis
from lib.event import Event
from entrypoint import settings

r = redis.Redis(**settings.settings_factory().redis_settings)


async def publish(channel, event: Event):
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe("task")
    print(
        f"********************** Publishing event {channel} **************************"
    )
    r.publish("task", json.dumps({"task": channel, "event": event.json()}))
    print(
        f"********************** Published event {channel} **************************"
    )
