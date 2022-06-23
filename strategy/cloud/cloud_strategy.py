import os

from azure.eventhub import EventData
from dotenv import load_dotenv

from strategy.cloud.redis_utils import RedisUtils
from strategy.utils import Strategy

from azure.eventhub.aio import EventHubProducerClient

import redis

load_dotenv()
my_redis_hostname = os.getenv("REDIS_HOST")
my_redis_password = os.getenv("REDIS_PASSWORD")
connect_eventhub_str = os.getenv("EVENTHUB_CONNECT_LINK")
eventhub_name = os.getenv("EVENTHUB_NAME")
redis_manager = redis.StrictRedis(host=my_redis_hostname, port=6380,
                                  password=my_redis_password, ssl=True, decode_responses=True)

producer = EventHubProducerClient.from_connection_string(
    conn_str=connect_eventhub_str,
    eventhub_name=eventhub_name)


class CloudStrategy(Strategy):
    def __init__(self, file_url):
        self.url = file_url

    async def do_algorithm(self, data):
        increment = 0
        utils = RedisUtils(total_data_count=len(data), redis=redis_manager)
        if not utils.is_new_file(self.url):
            return
        try:
            async with producer:
                for i in data[:15]:
                    event_data_batch = await producer.create_batch()
                    event_data_batch.add(EventData(str(i)))
                    await producer.send_batch(event_data_batch)
                    increment += 1
                    utils.update_file_progress(increment=increment)

        except(Exception,) as error:
            utils.update_file_status(status=error)
        print(f"Cloud response:\n{data}")
