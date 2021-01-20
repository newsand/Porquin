import json
import os


class Configleton:
    __instance__ = None
    _CONFIG_FILE = None
    _CONFIG: [dict] = None
    _PORQUIN_FILE = None
    _USER = None
    _BGC = None

    def __init__(self):
        if Configleton.__instance__ is None:
            Configleton.__instance__ = self
        else:
            raise Exception("You cannot instantiate another Configleton class")
        self.shared_instance().start('config.conf')

    @staticmethod
    def shared_instance():
        if not Configleton.__instance__:
            Configleton()
        return Configleton.__instance__

    def start(self, config_file=None):
        if config_file is None:
            config_file = get_required_env_var("CONFIG_FILE")
        assert os.path.exists(config_file)
        self._CONFIG_FILE = config_file
        with open(config_file, 'r') as f:
            self._CONFIG = json.load(f)

    def get_required_config_var(self, configvar: str) -> str:
        assert self._CONFIG
        if configvar not in self._CONFIG:
            raise Exception(f"Please set the {configvar} variable in the config file {self._CONFIG_FILE}")
        return self._CONFIG[configvar]

    def reset(self) -> None:
        self._PORQUIN_FILE = None
        self._CONFIG = None
        self._BGC = None

    def set_cryptkey(self, key):
        if 'CRYPT_KEY' in os.environ:
            raise Exception(f" {'CRYPT_KEY'} already set!")
        os.environ['CRYPT_KEY'] = key

    def get_cryptokey(self) -> str:
        if 'CRYPT_KEY' not in os.environ:
            raise Exception(f"Please set the {'CRYPT_KEY'} environment variable")
        return os.environ['CRYPT_KEY']

    @property
    def USER(self):
        return self._USER


def get_required_env_var(envvar: str) -> str:
    if envvar not in os.environ:
        raise Exception(f"Please set the {envvar} environment variable")
    return os.environ[envvar]
