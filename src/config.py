import src.ctn_config as cfg


class Config:
    def __init__(self):
        self.cfg = cfg

    def get_file_path(self):
        return self.cfg.file_path

    def get_survey_id(self):
        return self.cfg.survey_id

    def get_api_token(self):
        return self.cfg.api_token
