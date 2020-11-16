from dataclasses import dataclass
from datetime import datetime


def to_string(confidentiality_date: str) -> str:
    # Date string is: 2020-09-08 13:30:54,
    # corresponding to format '%Y-%m-%d %H:%M:%S'.
    # Output '%m/%d/%Y', but without leading zeros so the date is 9/8/2020.

    conf_date = datetime.strptime(confidentiality_date, '%Y-%m-%d %H:%M:%S')
    return f'{conf_date.month}/{conf_date.day}/{conf_date:%Y}'


@dataclass
class Person:
    """A simple dataclass holding some common data that will be written to the tracking sheet"""
    first_name: str
    last_name: str
    uo_id: str
    duck_id: str
    position_type: str
    supervisor: str
    confidentiality_date: str
    era_commons_id: str
    prox: str

    def to_list(self):
        return [self.first_name, self.last_name, self.uo_id, self.position_type, '',
                '', '', self.supervisor, '', self.duck_id,
                '', '', to_string(self.confidentiality_date), '', '',
                '', '', '', '', '',
                '', '', self.era_commons_id, '', '', '', self.prox]
