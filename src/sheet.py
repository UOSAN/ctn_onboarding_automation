from openpyxl import load_workbook
from .person import Person


class Sheet:
    def __init__(self, file_name: str):
        self._wb = load_workbook(filename=file_name)
        self._file_name = file_name

    def add_person(self, person: Person):
        ws = self._wb.active
        ws.append(person.to_list())
        self._wb.save(self._file_name)

    def find_person(self, person: Person):
        ws = self._wb.active
        found = False
        for row in ws.iter_rows(max_col=2):
            last_name, first_name = row
            if last_name == person.last_name and first_name == person.first_name:
                found = True

        return found
