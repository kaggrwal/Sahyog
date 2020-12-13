import enum


class UserType(enum.Enum):
    Donor = 'donor'
    Volunteer = 'volunteer'
    ScrapCollector = 'scrap_collector'
    Admin = 'admin'


