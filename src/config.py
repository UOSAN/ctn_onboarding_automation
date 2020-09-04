import json
import logging


class Config:
    def __init__(self, path: str = None):
        """
        Create an Config instance to read application configuration.

        :param str path: Path to configuration
        """
        logging.getLogger().info(f' Configuration path is: {path}')
        self._config_path = path
        self._file_path = None
        self._survey_id = None
        self._client_id = None
        self._clients = None

    def _read_config(self):
        if self._config_path:
            with open(self._config_path) as f:
                configuration = json.load(f)
                self._file_path = configuration['file_path']
                self._survey_id = configuration['survey_id']
                self._client_id = configuration['client_id']
                self._clients = configuration['clients']

    def get_file_path(self):
        if self._file_path is None:
            self._read_config()
        return self._file_path

    def get_survey_id(self):
        if self._survey_id is None:
            self._read_config()
        return self._survey_id

    def get_client_id(self):
        if self._client_id is None:
            self._read_config()
        return self._client_id

    def get_clients(self):
        if self._clients is None:
            self._read_config()
        return self._clients
