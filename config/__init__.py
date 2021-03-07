import logging
import os

import yaml

logger = logging.getLogger(__name__)

default = 'default'
env = os.environ.get('ENV', 'dev')


def replace_config_env(env, default_config):
    for key, value in default_config.items():
        default_config[key] = value.replace('{{env}}', env) if type(
            value) is str else value

    return default_config


def _load_config_from_file(env):
    with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
        try:
            configuration = yaml.safe_load(file)
            config = replace_config_env(env, configuration[default])
            config.update(configuration[env])
            config['env'] = env
            return config
        except yaml.YAMLError:
            logger.exception('Failed to load config from file')
            return None


config = _load_config_from_file(env)
