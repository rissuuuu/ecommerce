import asyncio
import json
import redis
from entrypoint import settings


r = redis.Redis(**settings.settings_factory().redis_settings)


async def main():
    print("entered")
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("task")  # (1)

    for m in pubsub.listen():
        data = json.loads(m["data"].decode("utf-8"))
        task = data["task"]
        if task == "seller_added":
            await seller_added(data["event"])



async def seller_added(data):
    print("***********************  SELLER ADDED  ******************************")
    print(data)




if __name__ == "__main__":
    asyncio.run(main())
