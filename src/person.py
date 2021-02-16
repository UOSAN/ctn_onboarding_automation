from dataclasses import dataclass

from src.utils import to_string


@dataclass
class Person:
    """A simple dataclass holding some common data that will be written to the tracking sheet."""
    first_name: str
    last_name: str
    uo_id: str
    duck_id: str
    position_type: str
    supervisor: str
    confidentiality_date: str
    era_commons_id: str
    prox: str

    def to_list(self, note: str):
        return [self.last_name, self.first_name, self.uo_id, self.position_type,
                '',  # Employee class
                '',  # Title
                '',  # PI
                self.supervisor,
                '',  # Project
                self.duck_id,
                '',  # CITI expiration
                '',  # GCP expiration
                to_string(self.confidentiality_date),
                '',  # Background cleared
                '',  # Student FERPA release
                '',  # Volunteer FY16 risk form
                '',  # Volunteer FY16 risk form
                '',  # Volunteer FY17 risk form
                '',  # Volunteer FY18 risk form
                '',  # Volunteer FY19 risk form
                '',  # Volunteer FY20 risk form
                '',  # Volunteer FY21 risk form
                '',  # Personal vehicle
                self.era_commons_id,
                '',  # eRA Commons role
                '',  # Individual office keys
                self.prox,
                '',  # LISB Exterior
                '',  # LISB 1st Floor
                '',  # LISB 2nd Floor
                '',  # LISB 3rd Floor
                '',  # LISB 340/423
                '',  # LISB Mgmt/Submaster
                '',  # STB Exterior
                '',  # STB Basement
                '',  # STB 064
                '',  # LCNI
                '',  # PSI Exterior
                '',  # PSI 103 Punch Code
                '',  # PSI 107 Punch Code
                '',  # PSI Common Key
                '',  # Bike Cages
                '',  # Other Access/Keys
                note  # Notes
                ]
