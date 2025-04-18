import redis.asyncio as redis
from src.configs.app_config import configure

config = configure()
keydb = redis.Redis(host=config.keydb.host, port=config.keydb.port, db=config.keydb.db)
