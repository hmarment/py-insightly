# -*- coding: utf-8 -*-


class Address(object):

    def __init__(self, street=None, city=None, state=None, post_code=None, country=None):
        self.street = street
        self.city = city
        self.state = state
        self.post_code = post_code
        self.country = country
