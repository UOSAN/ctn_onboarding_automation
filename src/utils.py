from datetime import datetime


def to_string(qualtrics_date: str) -> str:
    """
    Convert datetime string to month/day/year format.

    :param qualtrics_date: datetime string in format '%Y-%m-%d %H:%M:%S'
    :return: a string representing the same datetime in format '%m/%d/%Y'
    """
    # Date string is: 2020-09-08 13:30:54,
    # corresponding to format '%Y-%m-%d %H:%M:%S'.
    # Output '%m/%d/%Y', but without leading zeros so the date is 9/8/2020.

    conf_date = datetime.strptime(qualtrics_date, '%Y-%m-%d %H:%M:%S')
    return f'{conf_date.month}/{conf_date.day}/{conf_date:%Y}'
