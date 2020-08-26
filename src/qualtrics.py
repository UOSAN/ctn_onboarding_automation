import requests
from time import sleep
from typing import Optional
from src.config import Config


class QualtricsQuery:
    def __init__(self, config: Config):
        self._endpoint = 'https://ca1.qualtrics.com/API/v3'
        self._headers = {}
        self._timeout = 5
        self._survey_id = config.get_survey_id()
        self._client_id = config.get_client_id()
        self._clients = config.get_clients()

    def _get_token(self) -> None:
        """
        Get OAuth token for authorization.
        :return: None
        """
        url = f'https://ca1.qualtrics.com/oauth2/token'

        data = {'grant_type': 'client_credentials'}

        r = requests.post(url, auth=(self._client_id, self._clients), data=data)

        if r.status_code == requests.codes.ok:
            self._headers = {'Authorization': 'Bearer ' + r.json()['access_token']}

    def _create_response_export(self) -> Optional[str]:
        """
        Create a survey export from Qualtrics
        :return: A progress identifier
        """
        self._get_token()

        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses'

        request_data = {'format': 'csv', 'compress': 'false', 'useLabels': 'true'}
        r = requests.post(url=url, json=request_data, headers=self._headers, timeout=self._timeout)
        export_progress_id = None
        if r.status_code == requests.codes.ok:
            export_progress_id = r.json()['result']['progressId']
        return export_progress_id

    def _get_response_export_progress(self, export_progress_id: Optional[str]) -> Optional[str]:
        """
        Get the fileId of the survey export, by repeatedly querying for progress until the status is complete
        :param export_progress_id: A progress identifier
        :return: A file identifier
        """
        if not export_progress_id:
            raise ValueError('Invalid export progressId')

        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses/{export_progress_id}'
        r = requests.get(url=url, headers=self._headers, timeout=self._timeout)
        max_count = 10
        count = 0
        while r.status_code == requests.codes.ok and r.json()['result']['status'] != 'complete' and count < max_count:
            sleep(2)
            r = requests.get(url=url, headers=self._headers)
            count += 1

        file_id = None
        if r.status_code == requests.codes.ok and r.json()['result']['status'] == 'complete':
            file_id = r.json()['result']['fileId']

        return file_id

    def _get_response_export_file(self, file_id: str):
        """
        Get the exported survey results
        :param file_id: File identifier of the exported survey
        :return: A string in JSON format containing all survey responses
        """
        # No type hints on the return value of qualtrics_get_response_export_file because it is a big blob of JSON.
        if not file_id:
            raise ValueError('Invalid fileId. Did response export complete correctly?')

        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses/{file_id}/file'
        r = requests.get(url=url, headers=self._headers, timeout=self._timeout)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise ValueError('Could not get JSON response of surveys')

    def get_survey_response(self) -> str:
        export_progress_id = self._create_response_export()
        file_id = self._get_response_export_progress(export_progress_id)
        return self._get_response_export_file(file_id)
