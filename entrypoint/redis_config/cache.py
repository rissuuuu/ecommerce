from aiocache import caches

caches.set_config(
    {
        "default": {
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.StringSerializer"},
        },
        "redis_cache": {
            "cache": "aiocache.RedisCache",
            "endpoint": "127.0.0.1",
            "port": 6379,
            "timeout": 1,
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            "plugins": [
                {"class": "aiocache.plugins.HitMissRatioPlugin"},
                {"class": "aiocache.plugins.TimingPlugin"},
            ],
        },
    }
)
