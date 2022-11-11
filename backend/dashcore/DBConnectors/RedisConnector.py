from redis import Redis


class RedisConnector:
    def __init__(self):
        self.config = get_config()
        self.redis = Redis


    def init_connection(self):
        pass

