import csv
import io
import os
import sys

from src.config import Config
from src.person import Person
from src.qualtrics import QualtricsQuery
from src.sheet import Sheet

if __name__ == '__main__':
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path = os.path.abspath(os.path.join(bundle_dir, 'config.json'))

    config = Config(path)

    q = QualtricsQuery(config)
    responses = q.get_survey_response()

    f = io.StringIO(responses)
    reader = csv.reader(f)
    try:
        tracking_sheet = Sheet(config.get_file_path())
    except FileNotFoundError as e:
        print(f'Unable to find the tracking sheet at \'{config.get_file_path()}\'.')
        print(f'Check that you are connected to UO VPN and have connected to the CAS file server.')
        sys.exit()

    for i, r in enumerate(reader):
        # Skip first three rows
        if i < 3:
            continue
        # for each response, verify that the person is in the workbook. If they are not, add them
        # Columns start counting from 0 (first column is column 0)
        p = Person(first_name=r[17],
                   last_name=r[18],
                   uo_id=r[30],
                   duck_id=r[28],
                   position_type=r[24],
                   supervisor=r[22],
                   confidentiality_date=r[0],
                   era_commons_id=r[32],
                   prox=r[29])
        if not tracking_sheet.find_person(p):
            tracking_sheet.add_person(p)
