import os
import logging.config
import yaml


def setup_logging(path=None):
    if not path:
        path = os.path.join(os.path.dirname(__file__), "../data/log/config.yaml")

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError("Logging configuration file not found at {}".format(path))
