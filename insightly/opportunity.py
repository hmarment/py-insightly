# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str
from insightly.custom_field import CustomField
from insightly.exceptions import DoesNotExist
from insightly.link import Link
from insightly.models import DatetimeHandler
from insightly.helpers import parse_activity_date

import os
import yaml
import json
import datetime
import jsonpickle

# set serialisation for objects per Insightly API requirements
jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)

config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(config_file_path) as config_file:
    Config = yaml.load(config_file)


class Opportunity(InsightlyBase):
    """
    Class representing an Insightly Opportunity. Opportunity attributes are stored as normal
    Python attributes; access to all sub-objects, however, is always
    an API call (Links).
    """

    def __init__(self, client, opportunity_id=None, opportunity_name=None, opportunity_details=None,
                 organisation_id=None, owner_user_id=None, bid_amount=None, bid_currency=None, bid_duration=None,
                 bid_type=None, deletable=None, editable=None, category_id=None, customfields=None,
                 created=None, last_updated=None, forecast_close_date=None, actual_close_date=None, image_url=None,
                 links=None, opportunity_state=None, opportunity_state_reason_id=None, opportunity_value=None,
                 pipeline_id=None, probability=None, responsible_user_id=None, stage_id=None, tags=None,
                 visible_team_id=None, visible_to=None, visible_user_ids=None):
        """
        :client: Insightly API client
        :opportunity_id: ID for the Opportunity

        """
        super(Opportunity, self).__init__()
        self.client = client
        self.OPPORTUNITY_ID = opportunity_id
        self.OPPORTUNITY_NAME = opportunity_name
        self.OPPORTUNITY_DETAILS = opportunity_details
        self.ORGANISATION_ID = organisation_id
        self.OWNER_USER_ID = owner_user_id

        self.BID_AMOUNT = bid_amount
        self.BID_CURRENCY = bid_currency
        self.BID_DURATION = bid_duration
        self.BID_TYPE = bid_type
        self.CAN_DELETE = deletable
        self.CAN_EDIT = editable
        self.CATEGORY_ID = category_id
        self.CUSTOMFIELDS = customfields
        self.FORECAST_CLOSE_DATE = forecast_close_date
        self.ACTUAL_CLOSE_DATE = actual_close_date
        self.IMAGE_URL = image_url
        self.LINKS = links
        self.OPPORTUNITY_STATE = opportunity_state
        self.OPPORTUNITY_STATE_REASON_ID = opportunity_state_reason_id
        self.OPPORTUNITY_VALUE = opportunity_value
        self.PIPELINE_ID = pipeline_id
        self.PROBABILITY = probability
        self.RESPONSIBLE_USER_ID = responsible_user_id
        self.STAGE_ID = stage_id
        self.TAGS = tags
        self.VISIBLE_TEAM_ID = visible_team_id
        self.VISIBLE_TO = visible_to
        self.VISIBLE_USER_IDS = visible_user_ids

        if created:
            self.DATE_CREATED_UTC = parse_activity_date(created)
        if last_updated:
            self.DATE_UPDATED_UTC = parse_activity_date(last_updated)

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['client']
        del state['id']
        if state['OPPORTUNITY_ID'] is None:
            del state['OPPORTUNITY_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, insightly_client=None, json_obj=None):
        """
        Deserialize the organisation json object to an Opportunity object

        :insightly_client: the insightly client
        :json_obj: the opportunity json object
        """

        opportunity = Opportunity(client=insightly_client, opportunity_id=json_obj['OPPORTUNITY_ID'],
                                  opportunity_name=json_obj['OPPORTUNITY_NAME'],
                                  opportunity_details=json_obj['OPPORTUNITY_DETAILS'],
                                  organisation_id=json_obj['ORGANISATION_ID'],
                                  owner_user_id=json_obj['OWNER_USER_ID'],
                                  bid_amount=json_obj['BID_AMOUNT'],
                                  bid_currency=json_obj['BID_CURRENCY'],
                                  bid_duration=json_obj['BID_DURATION'],
                                  bid_type=json_obj['BID_TYPE'],
                                  deletable=json_obj['CAN_DELETE'],
                                  editable=json_obj['CAN_EDIT'],
                                  category_id=json_obj['CATEGORY_ID'],
                                  customfields=[CustomField.from_json(obj) for obj in json_obj['CUSTOMFIELDS']],
                                  forecast_close_date=json_obj['FORECAST_CLOSE_DATE'],
                                  actual_close_date=json_obj['ACTUAL_CLOSE_DATE'],
                                  image_url=json_obj['IMAGE_URL'],
                                  links=[Link.from_json(obj) for obj in json_obj['LINKS']],
                                  opportunity_state=json_obj['OPPORTUNITY_STATE'],
                                  opportunity_state_reason_id=json_obj['OPPORTUNITY_STATE_REASON_ID'],
                                  opportunity_value=json_obj['OPPORTUNITY_VALUE'],
                                  pipeline_id=json_obj['PIPELINE_ID'],
                                  probability=json_obj['PROBABILITY'],
                                  responsible_user_id=json_obj['RESPONSIBLE_USER_ID'],
                                  stage_id=json_obj['STAGE_ID'],
                                  tags=json_obj['TAGS'],
                                  visible_team_id=json_obj['VISIBLE_TEAM_ID'],
                                  visible_to=json_obj['VISIBLE_TO'],
                                  visible_user_ids=json_obj['VISIBLE_USER_IDS'],
                                  created=json_obj['DATE_CREATED_UTC'],
                                  last_updated=json_obj['DATE_UPDATED_UTC'])

        return opportunity

    def __repr__(self):
        return force_str(u'<Opportunity {}  {}>'.format(self.OPPORTUNITY_ID, self.OPPORTUNITY_NAME))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)

    def fetch(self):
        """Fetch all attributes for this Organisation"""
        json_obj = self.client.get_json(Config["Opportunities"]["Endpoints"]["Get"]["Url"]
                                        .format(id=self.OPPORTUNITY_ID),
                                        http_method=Config["Opportunities"]["Endpoints"]["Get"]["Method"])
        self.from_json(json_obj=json_obj)

    def save(self):
        """ Create or update  """
        if self.OPPORTUNITY_ID is None:  # create a new opportunity
            json_obj = self.client.get_json(
                    Config["Opportunities"]["Endpoints"]["Add"]["Url"],
                    http_method=Config["Opportunities"]["Endpoints"]["Add"]["Method"],
                    post_args=json.loads(self.to_json()))
            # Set initial data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)
            self.OPPORTUNITY_ID = json_obj["OPPORTUNITY_ID"]
        else:  # update existing opportunity
            json_obj = self.client.get_json(
                Config["Opportunities"]["Endpoints"]["Update"]["Url"].format(id=self.OPPORTUNITY_ID),
                http_method=Config["Opportunities"]["Endpoints"]["Update"]["Method"],
                post_args=json.loads(self.to_json()))
            # Set new data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)

    def get_link(self, link_id):
        """Get a link for this organisation
        :link_id: the identifier for the link
        :return: the link
        :rtype: Link
        """
        # TODO: make this type specific to ensure correct updates
        link = None

        for check_link in self.LINKS:
            if check_link.LINK_ID == link_id:
                link = link_id

        return link

    def add_contact_link(self, contact_id, role=None, details=None):
        """Add a contact link to this opportunity

        :contact_id: Contact ID to link to this Opportunity
        :role: role in this Opportunity
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(OPPORTUNITY_ID=self.OPPORTUNITY_ID, CONTACT_ID=contact_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Opportunities"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=self.OPPORTUNITY_ID),
                                        http_method=Config["Opportunities"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_contact_link(self, link_id=None, contact_id=None, role=None, details=None):
        """Update a contact link to this Opportunity
        :link_id: the identifier for the opportunity link - note: must exist already in order to update
        :contact_id: Contact ID to link to this Opportunity
        :role: role in this Opportunity
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        link = self.get_link(link_id)

        if not link:
            raise DoesNotExist("Contact Link does not exist", link)

        post_args = dict(LINK_ID=link_id,
                         CONTACT_ID=contact_id if contact_id else link.CONTACT_ID)

        if role:
            post_args['ROLE'] = role
        if not role and link.ROLE:
            post_args['ROLE'] = link.ROLE

        if details:
            post_args['DETAILS'] = details
        if not details and link.DETAILS:
            post_args['DETAILS'] = link.DETAILS

        json_obj = self.client.get_json(Config["Opportunities"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=self.OPPORTUNITY_ID),
                                        http_method=Config["Opportunities"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def add_organisation_link(self, organisation_id, role=None, details=None):
        """Add a organisation link to this opportunity

        :organisation_id: Organisation ID to link to this Opportunity
        :role: role in this Opportunity
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(OPPORTUNITY_ID=self.OPPORTUNITY_ID, ORGANISATION_ID=organisation_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Opportunities"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=self.OPPORTUNITY_ID),
                                        http_method=Config["Opportunities"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_organisation_link(self, link_id=None, organisation_id=None, role=None, details=None):
        """Update a organisation link to this Opportunity
        :link_id: the identifier for the organisation link - note: must exist already in order to update
        :organisation_id: Organisation ID to link to this Opportunity
        :role: role in this Opportunity
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        link = self.get_link(link_id)

        if not link:
            raise DoesNotExist("Organisation Link does not exist", link)

        post_args = dict(LINK_ID=link_id,
                         ORGANISATION_ID=organisation_id if organisation_id else link.ORGANISATION_ID)

        if role:
            post_args['ROLE'] = role
        if not role and link.ROLE:
            post_args['ROLE'] = link.ROLE

        if details:
            post_args['DETAILS'] = details
        if not details and link.DETAILS:
            post_args['DETAILS'] = link.DETAILS

        json_obj = self.client.get_json(Config["Opportunities"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=self.OPPORTUNITY_ID),
                                        http_method=Config["Opportunities"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def get_custom_field_by_field_name(self, field_name):
        """Get a custom for this opportunity from the Insightly Field Name - note: these are defined by adsquare in the
        adsquare Insightly account.

        :field_name: the field name for the custom field e.g. DESTINATION_PARTNER__c, note: these are always suffixed by
                     '__c'.
        :return: the custom field
        :rtype: CustomField
        """

        for custom_field in self.CUSTOMFIELDS:
            if custom_field.CUSTOM_FIELD_ID == field_name:
                return custom_field


class OpportunityCategory(InsightlyBase):
    """
    Class representing an Insightly Opportunity Category.
    """

    def __init__(self, category_id=None, category_name=None, active=None, background_color=None):
        super(OpportunityCategory, self).__init__()
        self.CATEGORY_ID = category_id
        self.CATEGORY_NAME = category_name
        self.ACTIVE = active
        self.BACKGROUND_COLOR = background_color

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the opportunity category json object to an Opportunity Category object

        :json_obj: the opportunity json object
        """

        opportunity_category = OpportunityCategory(category_id=json_obj['CATEGORY_ID'],
                                                   category_name=json_obj['CATEGORY_NAME'],
                                                   active=json_obj['ACTIVE'],
                                                   background_color=json_obj['BACKGROUND_COLOR'])

        return opportunity_category

    def __repr__(self):
        return force_str(u'<Opportunity Category {}  {}>'.format(self.CATEGORY_ID, self.CATEGORY_NAME))