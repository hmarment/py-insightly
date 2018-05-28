# -*- coding: utf-8 -*-

import jsonpickle


class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    """ Serialise Datetime objects in required format for Insightly API """

    def flatten(self, obj, data):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
