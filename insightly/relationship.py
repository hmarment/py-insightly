# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str

import os
import yaml
import json

# set serialisation for objects per Insightly API requirements
# jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)

config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(config_file_path) as config_file:
    Config = yaml.load(config_file, Loader=yaml.FullLoader)


class Relationship(InsightlyBase):
    """
    Class representing an Insightly Relationship. Relationship attributes are stored as normal
    Python attributes. Currently just a basic class - as of version 2.3, Insightly does not offer APIs to manage
    Relationships
    """

    def __init__(self, relationship_id=None, forward_title=None, forward=None, reverse_title=None,
                 reverse=None, for_contacts=False, for_organisations=False):
        """
        :client: Insightly API client
        :relationship_id: ID for the Relationship
        """
        super(Relationship, self).__init__()
        self.RELATIONSHIP_ID = relationship_id
        self.FORWARD_TITLE = forward_title
        self.FORWARD = forward

        self.REVERSE_TITLE = reverse_title
        self.REVERSE = reverse
        self.FOR_CONTACTS = for_contacts
        self.FOR_ORGANISATIONS = for_organisations

    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     del state['client']
    #     return state
    #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)

    def __repr__(self):
        return force_str(u'<Relationship {}  {}>'.format(self.RELATIONSHIP_ID, self.FORWARD_TITLE))

    def to_json(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']

        return json.dumps(state, default=str)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the relationship json object to a Relatioship object

        :insightly_client: the insightly client
        :json_obj: the relationship json object
        """

        relationship = Relationship(relationship_id=json_obj['RELATIONSHIP_ID'],
                                    forward_title=json_obj['FORWARD_TITLE'],
                                    forward=json_obj['FORWARD'],
                                    reverse_title=json_obj['REVERSE_TITLE'],
                                    reverse=json_obj['REVERSE'],
                                    for_contacts=json_obj['FOR_CONTACTS'],
                                    for_organisations=json_obj['FOR_ORGANISATIONS'])

        return relationship
