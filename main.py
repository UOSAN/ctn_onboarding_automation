from src.qualtrics import QualtricsQuery
from src.config import Config
from src.person import Person
from src.sheet import Sheet
import io
import csv


if __name__ == '__main__':
    config = Config('instance')
    tracking_sheet = Sheet(config.get_file_path())
    q = QualtricsQuery(config.get_survey_id(), config.get_api_token())
    responses = q.get_survey_response()

    f = io.StringIO(responses)
    reader = csv.reader(f)
    for i, r in enumerate(reader):
        # Skip first three rows
        if i < 3:
            continue
        # for each response, verify that the person is in the workbook. If they are not, add them
        # 'column 17' -> position_type
        # 'column 18' -> first_name
        # 'column 19' -> last_name
        # 'column 38' -> ou_id (95 number)
        # 'column 40' -> duck_id
        p = Person(r[44],
                   r[45],
                   r[59],
                   r[61],
                   r[17])
        if not tracking_sheet.find_person(p):
            tracking_sheet.add_person(p)
