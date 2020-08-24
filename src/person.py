from dataclasses import dataclass


@dataclass
class Person:
    """A simple dataclass holding some common data that will be written to the tracking sheet"""
    first_name: str
    last_name: str
    uo_id: str
    duck_id: str
    position_type: str

    def to_list(self):
        return [self.first_name, self.last_name, self.uo_id, self.position_type, '',
                '', '', '', '', self.duck_id]
