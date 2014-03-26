
class Server(object):
    def __init__(self, config):
        self.config = config


def create_server(config=None):
    if config is None:
        config = {}
    return Server(config)
