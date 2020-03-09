# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str
from insightly.helpers import parse_activity_date
from insightly.models import DatetimeHandler

import os
import yaml
import json
import datetime
import jsonpickle

# set serialisation for objects per Insightly API requirements
jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)

config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(config_file_path) as config_file:
    Config = yaml.load(config_file, Loader=yaml.FullLoader)


class User(InsightlyBase):
    """
    Class representing an Insightly User. User attributes are stored as normal
    Python attributes. Currently just a basic class - as of version 2.3, Insightly does not offer APIs to manage
    Users
    """

    def __init__(self, client, user_id=None, first_name=None, last_name=None, email_address=None,
                 admin=False, active=True, contact_id=None, contact_display=None, contact_order=None, instance_id=None,
                 account_owner=None, timezone_id=None, user_currency=None, task_week_start=None,
                 email_dropbox_address=None, email_dropbox_identifier=None, created=None, last_updated=None):
        """
        :client: Insightly API client
        :user_id: ID for the User
        """
        super(User, self).__init__()
        self.client = client
        self.USER_ID = user_id
        self.FIRST_NAME = first_name
        self.LAST_NAME = last_name
        self.EMAIL_ADDRESS = email_address
        self.ADMINISTRATOR = admin
        self.ACTIVE = active
        self.CONTACT_ID = contact_id
        self.CONTACT_DISPLAY = contact_display
        self.CONTACT_ORDER = contact_order
        self.INSTANCE_ID = instance_id

        self.ACCOUNT_OWNER = account_owner
        self.TIMEZONE_ID = timezone_id
        self.USER_CURRENCY = user_currency
        self.TASK_WEEK_START = task_week_start
        self.EMAIL_DROPBOX_ADDRESS = email_dropbox_address
        self.EMAIL_DROPBOX_IDENTIFIER = email_dropbox_identifier

        if created:
            self.DATE_CREATED_UTC = parse_activity_date(created)
        if last_updated:
            self.DATE_UPDATED_UTC = parse_activity_date(last_updated)

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['client']
        del state['id']
        if state['USER_ID'] is None:
            del state['USER_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __repr__(self):
        return force_str(u'<User {}  {} {}>'.format(self.USER_ID, self.FIRST_NAME, self.LAST_NAME))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)

    @classmethod
    def from_json(cls, insightly_client=None, json_obj=None):
        """
        Deserialize the relationship json object to a User object

        :insightly_client: the insightly client
        :json_obj: the user json object
        """

        user = User(client=insightly_client, user_id=json_obj['USER_ID'],
                    first_name=json_obj['FIRST_NAME'],
                    last_name=json_obj['LAST_NAME'],
                    email_address=json_obj['EMAIL_ADDRESS'],
                    admin=json_obj['ADMINISTRATOR'],
                    active=json_obj['ACTIVE'],
                    contact_id=json_obj['CONTACT_ID'],
                    contact_display=json_obj['CONTACT_DISPLAY'],
                    contact_order=json_obj['CONTACT_ORDER'],
                    instance_id=json_obj['INSTANCE_ID'],
                    account_owner=json_obj['ACCOUNT_OWNER'],
                    timezone_id=json_obj['TIMEZONE_ID'],
                    user_currency=json_obj['USER_CURRENCY'],
                    task_week_start=json_obj['TASK_WEEK_START'],
                    email_dropbox_address=json_obj['EMAIL_DROPBOX_ADDRESS'],
                    email_dropbox_identifier=json_obj['EMAIL_DROPBOX_IDENTIFIER'],
                    created=json_obj['DATE_CREATED_UTC'],
                    last_updated=json_obj['DATE_UPDATED_UTC'])

        return user
