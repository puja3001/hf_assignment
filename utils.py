import datetime


def dateconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()