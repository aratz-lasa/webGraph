import os
import logging.config
import yaml


def setup_logging():
    path = "webGraph/data/log/config.yaml"
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        absolute_logging_config_file_path = os.path.realpath(path)
        raise FileNotFoundError("Logging configuration file not found at {}".format(absolute_logging_config_file_path))
