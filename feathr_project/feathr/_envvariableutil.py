import os
import yaml
from loguru import logger


class _EnvVaraibleUtil(object):
    @staticmethod
    def get_environment_variable_with_default(*args):
        """Gets the environment variable for the variable key.
        Args:
            *args: list of keys in feathr_config.yaml file
        Return:
            A environment variable for the variable key. If it's not set in the environment, then a default is retrieved
            from the feathr_config.yaml file with the same config key.
            """
        with open(os.path.abspath('feathr_config.yaml'), 'r') as stream:
            try:
                yaml_config = yaml.safe_load(stream)
                # concat all layers
                # check in environment variable
                yaml_layer = yaml_config
                env_keyword = "__".join(args)
                upper_env_keyword = env_keyword.upper()
                # make it work for lower case and upper case.
                env_variable = os.environ.get(env_keyword, os.environ.get(upper_env_keyword))
                if env_variable:
                    return env_variable
                # resolve one layer after another
                for arg in args:
                    yaml_layer = yaml_layer[arg]
                return yaml_layer
            except yaml.YAMLError as exc:
                logger.info(exc)

    @staticmethod
    def get_environment_variable(variable_key):
        """Gets the environment variable for the variable key.

        Args:
            variable_key: environment variable key that is used to retrieve the environment variable
        Return:
            A environment variable for the variable key.
        Raises:
            ValueError: If the environment variable is not set for this key, an exception is thrown.
            """
        password = os.environ.get(variable_key)
        if not password:
            logger.info(variable_key + ' is not set in the environment variables.')
        return password
