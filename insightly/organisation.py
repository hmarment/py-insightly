# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str
from insightly.custom_field import  CustomField
from insightly.exceptions import DoesNotExist
from insightly.link import Link, OrganisationLink
from insightly.models import Address
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
    Config = yaml.load(config_file, Loader=yaml.FullLoader)


class Organisation(InsightlyBase):
    """
    Class representing an Insightly Organisation. Organisation attributes are stored as normal
    Python attributes; access to all sub-objects, however, is always
    an API call (Lists, Cards).
    """

    def __init__(self, client, organisation_id=None, name='', background=None, billing_address=Address(),
                 shipping_address=Address(), deletable=True, editable=True, custom_fields=[],
                 dates=[], created=None, last_updated=None, email_domains=[], image_url=None, links=[],
                 organisation_links=[], owner_user_id=None, phone=None, fax=None, facebook=None, linkedin=None,
                 twitter=None, tags=[], visible_team_id=None, visible_to='EVERYONE', visible_user_ids=None,
                 website=None):
        """
        :client: Insightly API client
        :organisation_id: ID for the Organisation

        Alternative Constructor

        :organisation: reference to the parent Organisation
        :organisation_id: ID for this Organisation

        """
        super(Organisation, self).__init__()
        self.client = client
        self.ORGANISATION_ID = organisation_id
        self.ORGANISATION_NAME = name
        self.BACKGROUND = background

        self.ADDRESS_BILLING_CITY = billing_address.city
        self.ADDRESS_BILLING_COUNTRY = billing_address.country
        self.ADDRESS_BILLING_POSTCODE = billing_address.post_code
        self.ADDRESS_BILLING_STATE = billing_address.state
        self.ADDRESS_BILLING_STREET = billing_address.street

        self.ADDRESS_SHIP_CITY = shipping_address.city
        self.ADDRESS_SHIP_COUNTRY = shipping_address.country
        self.ADDRESS_SHIP_POSTCODE = shipping_address.post_code
        self.ADDRESS_SHIP_STATE = shipping_address.state
        self.ADDRESS_SHIP_STREET = shipping_address.street

        self.CAN_DELETE = deletable
        self.CAN_EDIT = editable

        self.CUSTOMFIELDS = custom_fields
        self.DATES = dates

        if created:
            self.DATE_CREATED_UTC = parse_activity_date(created)
        if last_updated:
            self.DATE_UPDATED_UTC = parse_activity_date(last_updated)

        self.EMAILDOMAINS = email_domains
        self.IMAGE_URL = image_url
        self.LINKS = links
        self.ORGANISATIONLINKS = organisation_links
        self.OWNER_USER_ID = owner_user_id
        self.PHONE = phone
        self.PHONE_FAX = fax
        self.SOCIAL_FACEBOOK = facebook
        self.SOCIAL_LINKEDIN = linkedin
        self.SOCIAL_TWITTER = twitter
        self.TAGS = tags
        self.VISIBLE_TEAM_ID = visible_team_id
        self.VISIBLE_TO = visible_to
        self.VISIBLE_USER_IDS = visible_user_ids
        self.WEBSITE = website

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['client']
        del state['id']
        if state['ORGANISATION_ID'] is None:
            del state['ORGANISATION_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, insightly_client=None, json_obj=None):
        """
        Deserialize the organisation json object to a Organisation object

        :insightly_client: the insightly client
        :json_obj: the organisation json object
        """

        organisation = Organisation(client=insightly_client, organisation_id=json_obj['ORGANISATION_ID'],
                                    name=json_obj['ORGANISATION_NAME'], background=json_obj['BACKGROUND'],
                                    billing_address=Address(json_obj['ADDRESS_BILLING_STREET'],
                                                            json_obj['ADDRESS_BILLING_CITY'],
                                                            json_obj['ADDRESS_BILLING_STATE'],
                                                            json_obj['ADDRESS_BILLING_POSTCODE'],
                                                            json_obj['ADDRESS_BILLING_COUNTRY']),
                                    shipping_address=Address(json_obj['ADDRESS_BILLING_STREET'],
                                                             json_obj['ADDRESS_BILLING_CITY'],
                                                             json_obj['ADDRESS_BILLING_STATE'],
                                                             json_obj['ADDRESS_BILLING_POSTCODE'],
                                                             json_obj['ADDRESS_BILLING_COUNTRY']),
                                    deletable=json_obj['CAN_DELETE'], editable=json_obj['CAN_EDIT'],
                                    custom_fields=[CustomField.from_json(obj) for obj in json_obj['CUSTOMFIELDS']],
                                    dates=json_obj['DATES'], created=json_obj['DATE_CREATED_UTC'],
                                    last_updated=json_obj['DATE_UPDATED_UTC'], email_domains=json_obj['EMAILDOMAINS'],
                                    image_url=json_obj['IMAGE_URL'],
                                    links=[Link.from_json(json_obj=obj) for obj in json_obj['LINKS']],
                                    organisation_links=[OrganisationLink.from_json(json_obj=obj)
                                                        for obj in json_obj['ORGANISATIONLINKS']],
                                    owner_user_id=json_obj['OWNER_USER_ID'], phone=json_obj['PHONE'],
                                    fax=json_obj['PHONE_FAX'], facebook=json_obj['SOCIAL_FACEBOOK'],
                                    linkedin=json_obj['SOCIAL_LINKEDIN'], twitter=json_obj['SOCIAL_TWITTER'],
                                    tags=json_obj['TAGS'], visible_team_id=json_obj['VISIBLE_TEAM_ID'],
                                    visible_to=json_obj['VISIBLE_TO'], visible_user_ids=json_obj['VISIBLE_USER_IDS'],
                                    website=json_obj['WEBSITE'])

        return organisation

    def __repr__(self):
        return force_str(u'<Organisation {}  {}>'.format(self.ORGANISATION_ID, self.ORGANISATION_NAME))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)

    def fetch(self):
        """Fetch all attributes for this Organisation"""
        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["Get"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["Get"]["Method"])
        self.from_json(json_obj=json_obj)

    def save(self):
        """ Create or update  """
        if self.ORGANISATION_ID is None:  # create a new organisation
            json_obj = self.client.get_json(
                    Config["Organisations"]["Endpoints"]["Add"]["Url"],
                    http_method=Config["Organisations"]["Endpoints"]["Add"]["Method"],
                    post_args=json.loads(self.to_json()))
            # Set initial data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)
            self.ORGANISATION_ID = json_obj["ORGANISATION_ID"]
        else:  # update existing organisation
            json_obj = self.client.get_json(
                Config["Organisations"]["Endpoints"]["Update"]["Url"].format(id=self.ORGANISATION_ID),
                http_method=Config["Organisations"]["Endpoints"]["Update"]["Method"],
                post_args=json.loads(self.to_json()))
            # Set new data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)

    def get_organisation_link(self, organisation_link_id):
        """Get an organisation link for this organisation
        :organisation_link_id: the identifier for the organisation link
        :return: the organisation link
        :rtype: OrganisationLink
        """

        organisation_link = None

        for org_link in self.ORGANISATIONLINKS:
            if org_link.ORG_LINK_ID == organisation_link_id:
                organisation_link = org_link

        return organisation_link

    def add_organisation_link(self, parent_organisation_id, child_organisation_id, relationship_id=7, details=None):
        """Add an organisation link to this organisation

        :parent_organisation_id: Organisation ID of the parent in the relationship
        :child_organisation_id: Organisation ID of the child in the relationship
        :relationship_id: identifier for the type of relationship, default = Parent / Subsidiary
        :details: additional details to add context
        :return: the organisation link
        :rtype: OrganisationLink
        """
        post_args = dict(FIRST_ORGANISATION_ID=child_organisation_id, SECOND_ORGANISATION_ID=parent_organisation_id,
                         RELATIONSHIP_ID=relationship_id)

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["AddOrganisationLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["AddOrganisationLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return OrganisationLink.from_json(json_obj)

    def update_organisation_link(self, organisation_link_id, parent_organisation_id=None, child_organisation_id=None,
                                 relationship_id=None, details=None):
        """Update an Organisation Link to this Organisation
        :organisation_link_id: the identifier for the organisation link - note: must exist already in order to update
        :parent_organisation_id: Organisation ID of the parent in the relationship
        :child_organisation_id: Organisation ID of the child in the relationship
        :relationship_id: identifier for the type of relationship, default = Parent / Subsidiary
        :details: additional details to add context
        :return: the organisation link
        :rtype: OrganisationLink
        """

        organisation_link = self.get_organisation_link(organisation_link_id)

        if not organisation_link:
            raise DoesNotExist("Organisation Link does not exist", organisation_link_id)

        post_args = dict(ORG_LINK_ID=organisation_link_id,
                         FIRST_ORGANISATION_ID=child_organisation_id if child_organisation_id
                         else organisation_link.FIRST_ORGANISATION_ID,
                         SECOND_ORGANISATION_ID=parent_organisation_id if parent_organisation_id
                         else organisation_link.SECOND_ORGANISATION_ID,
                         RELATIONSHIP_ID=relationship_id if relationship_id else organisation_link.RELATIONSHIP_ID)

        if details:
            post_args['DETAILS'] = details
        if not details and organisation_link.DETAILS:
            post_args['DETAILS'] = organisation_link.DETAILS

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["UpdateOrganisationLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["UpdateOrganisationLink"][
                                            "Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return OrganisationLink.from_json(json_obj)

    def get_link(self, link_id):
        """Get a link for this organisation
        :link_id: the identifier for the link
        :return: the link
        :rtype: Link
        """
        # TODO: make this type specific to ensure correct updates
        link = None

        for check_link in self.ORGANISATIONLINKS:
            if check_link.LINK_ID == link_id:
                link = link_id

        return link

    def add_contact_link(self, contact_id, role=None, details=None):
        """Add a contact link to this organisation

        :contact_id: Contact ID to link to this Organisation
        :role: role in this Organisation
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(ORGANISATION_ID=self.ORGANISATION_ID, CONTACT_ID=contact_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_contact_link(self, link_id=None, contact_id=None, role=None, details=None):
        """Update a contact link to this Organisation
        :link_id: the identifier for the organisation link - note: must exist already in order to update
        :contact_id: Contact ID to link to this Organisation
        :role: role in this Organisation
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

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def add_opportunity_link(self, opportunity_id, role=None, details=None):
        """Add an opportunity link to this organisation

        :opportunity: Opportunity ID to link to this Organisation
        :role: role in this Organisation
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(ORGANISATION_ID=self.ORGANISATION_ID, OPPORTUNITY_ID=opportunity_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_opportunity_link(self, link_id=None, opportunity_id=None, role=None, details=None):
        """Update a opportunity link to this Organisation
        :link_id: the identifier for the opportunity link - note: must exist already in order to update
        :opportunity_id: Opportunity ID to link to this Organisation
        :role: role in this Organisation
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        link = self.get_link(link_id)

        if not link:
            raise DoesNotExist("Opportunity Link does not exist", link)

        post_args = dict(LINK_ID=link_id,
                         OPPORTUNITY_ID=opportunity_id if opportunity_id else link.OPPORTUNITY_ID)

        if role:
            post_args['ROLE'] = role
        if not role and link.ROLE:
            post_args['ROLE'] = link.ROLE

        if details:
            post_args['DETAILS'] = details
        if not details and link.DETAILS:
            post_args['DETAILS'] = link.DETAILS

        json_obj = self.client.get_json(Config["Organisations"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=self.ORGANISATION_ID),
                                        http_method=Config["Organisations"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)
