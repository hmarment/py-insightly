# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str

import jsonpickle


class CustomField(InsightlyBase):
    """
    Class representing an Insightly Custom Field - i.e. information to be stored on different entity types as defined
    in our own account.
    """

    def __init__(self, custom_field_id=None, custom_field_value=None):

        super(CustomField, self).__init__()
        self.CUSTOM_FIELD_ID = custom_field_id
        self.FIELD_VALUE = custom_field_value

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the contact json object to a OrganisationLink object

        :json_obj: the contact link object
        """

        custom_field = CustomField(custom_field_id=json_obj['CUSTOM_FIELD_ID'],
                                   custom_field_value=json_obj['FIELD_VALUE'])

        return custom_field

    def __repr__(self):
        return force_str(u'<CustomField {}  {}>'.format(self.CUSTOM_FIELD_ID, self.FIELD_VALUE))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)