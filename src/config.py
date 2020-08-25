import json
import logging
import os


class Config:
    def __init__(self, path: str = None):
        """
        Create an Config instance to read application configuration.

        :param str path: Path to configuration
        """
        logging.getLogger().info(f' Configuration path is: {path}')
        print(path)
        self._config_path = path
        self._file_path = None
        self._survey_id = None
        self._api_token = None

    def _read_config(self):
        if self._config_path:
            print(os.path.join(self._config_path, 'config.json'))
            with open(os.path.join(self._config_path, 'config.json')) as f:
                configuration = json.load(f)
                self._file_path = configuration['file_path']
                self._survey_id = configuration['survey_id']
                self._api_token = configuration['api_token']

    def get_file_path(self):
        if self._file_path is None:
            self._read_config()
        return self._file_path

    def get_survey_id(self):
        if self._survey_id is None:
            self._read_config()
        return self._survey_id

    def get_api_token(self):
        if self._api_token is None:
            self._read_config()
        return self._api_token
