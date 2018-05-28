# -*- coding: utf-8 -*-

from dateutil import parser as dateparser


def parse_activity_date(date_string):
    """Return the date of an action.

    :rtype: datetime.datetime
    """
    return dateparser.parse(date_string)