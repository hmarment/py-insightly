# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str
from insightly.custom_field import CustomField
from insightly.exceptions import DoesNotExist
from insightly.link import ContactLink, Link
from insightly.models import Address, DatetimeHandler
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


class Contact(InsightlyBase):
    """
    Class representing an Insightly Contact. Contact attributes are stored as normal
    Python attributes; access to all sub-objects, however, is always
    an API call (Links, Custom Fields).
    """

    def __init__(self, client, contact_id=None, organisation_id=None, default_linked_organisation_id=None,
                 salutation=None, first_name='', last_name='', dob=None, email_address=None, title=None,
                 background=None, postal_address=Address(), other_address=Address(), assistant_name=None,
                 assistant_phone=None, deletable=True, editable=True, contact_links=[], custom_fields=[], dates=[],
                 created=None, last_updated=None, image_url=None, links=[], owner_user_id=None,
                 phone=None, fax=None, phone_home=None, phone_mobile=None, phone_other=None, facebook=None,
                 linkedin=None, twitter=None, tags=[], visible_team_id=None, visible_to='EVERYONE',
                 visible_user_ids=None,):
        """
        :client: Insightly API client
        :contact_id: ID for the Contact

        """
        super(Contact, self).__init__()
        self.client = client
        self.CONTACT_ID = contact_id
        self.ORGANISATION_ID = organisation_id
        self.DEFAULT_LINKED_ORGANISATION = default_linked_organisation_id
        self.SALUTATION = salutation
        self.FIRST_NAME = first_name
        self.LAST_NAME = last_name
        self.DATE_OF_BIRTH = dob
        self.EMAIL_ADDRESS = email_address
        self.TITLE = title
        self.BACKGROUND = background

        self.ADDRESS_MAIL_STREET = postal_address.street
        self.ADDRESS_MAIL_CITY = postal_address.city
        self.ADDRESS_MAIL_POSTCODE = postal_address.post_code
        self.ADDRESS_MAIL_STATE = postal_address.state
        self.ADDRESS_MAIL_COUNTRY = postal_address.country

        self.ADDRESS_OTHER_STREET = other_address.street
        self.ADDRESS_OTHER_CITY = other_address.city
        self.ADDRESS_OTHER_POSTCODE = other_address.post_code
        self.ADDRESS_OTHER_STATE = other_address.state
        self.ADDRESS_OTHER_COUNTRY = other_address.country

        self.ASSISTANT_NAME = assistant_name
        self.PHONE_ASSISTANT = assistant_phone
        self.CAN_DELETE = deletable
        self.CAN_EDIT = editable
        self.CONTACTLINKS = contact_links
        self.CUSTOMFIELDS = custom_fields
        self.DATES = dates
        self.IMAGE_URL = image_url
        self.LINKS = links
        self.OWNER_USER_ID = owner_user_id
        self.PHONE = phone
        self.PHONE_FAX = fax
        self.PHONE_HOME = phone_home
        self.PHONE_MOBILE = phone_mobile
        self.PHONE_OTHER = phone_other
        self.SOCIAL_FACEBOOK = facebook
        self.SOCIAL_LINKEDIN = linkedin
        self.SOCIAL_TWITTER = twitter
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
        if state['CONTACT_ID'] is None:
            del state['CONTACT_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, insightly_client=None, json_obj=None):
        """
        Deserialize the contact json object to a Contact object

        :insightly_client: the insightly client
        :json_obj: the contact json object
        """

        contact = Contact(client=insightly_client, contact_id=json_obj['CONTACT_ID'],
                          organisation_id=json_obj['ORGANISATION_ID'],
                          default_linked_organisation_id=json_obj['DEFAULT_LINKED_ORGANISATION'],
                          salutation=json_obj['SALUTATION'], first_name=json_obj['FIRST_NAME'],
                          last_name=json_obj['LAST_NAME'], dob=json_obj['DATE_OF_BIRTH'],
                          email_address=json_obj['EMAIL_ADDRESS'],
                          title=json_obj['TITLE'],
                          background=json_obj['BACKGROUND'],
                          postal_address=Address(json_obj['ADDRESS_MAIL_STREET'], json_obj['ADDRESS_MAIL_CITY'],
                                                 json_obj['ADDRESS_MAIL_STATE'], json_obj['ADDRESS_MAIL_POSTCODE'],
                                                 json_obj['ADDRESS_MAIL_COUNTRY']),
                          other_address=Address(json_obj['ADDRESS_OTHER_STREET'], json_obj['ADDRESS_OTHER_CITY'],
                                                json_obj['ADDRESS_OTHER_STATE'], json_obj['ADDRESS_OTHER_POSTCODE'],
                                                json_obj['ADDRESS_OTHER_COUNTRY']),
                          assistant_name=json_obj['ASSISTANT_NAME'], assistant_phone=json_obj['PHONE_ASSISTANT'],
                          deletable=json_obj['CAN_DELETE'], editable=json_obj['CAN_EDIT'],
                          contact_links=[ContactLink.from_json(obj) for obj in json_obj['CONTACTLINKS']],
                          custom_fields=[CustomField.from_json(obj) for obj in json_obj['CUSTOMFIELDS']],
                          dates=json_obj['DATES'], created=json_obj['DATE_CREATED_UTC'],
                          last_updated=json_obj['DATE_UPDATED_UTC'], image_url=json_obj['IMAGE_URL'],
                          links=[Link.from_json(obj) for obj in json_obj['LINKS']],
                          owner_user_id=json_obj['OWNER_USER_ID'], phone=json_obj['PHONE'],
                          fax=json_obj['PHONE_FAX'], phone_home=json_obj['PHONE_HOME'],
                          phone_mobile=json_obj['PHONE_MOBILE'], phone_other=json_obj['PHONE_OTHER'],
                          facebook=json_obj['SOCIAL_FACEBOOK'], linkedin=json_obj['SOCIAL_LINKEDIN'],
                          twitter=json_obj['SOCIAL_TWITTER'], tags=json_obj['TAGS'],
                          visible_team_id=json_obj['VISIBLE_TEAM_ID'],
                          visible_to=json_obj['VISIBLE_TO'], visible_user_ids=json_obj['VISIBLE_USER_IDS'])

        return contact

    def __repr__(self):
        return force_str(u'<Contact {}  {}>'.format(self.CONTACT_ID, force_str("{} {}".format(self.FIRST_NAME,
                                                                                              self.LAST_NAME))))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)

    def fetch(self):
        """Fetch all attributes for this Contact"""
        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["Get"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["Get"]["Method"])
        self.from_json(json_obj=json_obj)

    def save(self):
        """ Create or update  """
        if self.CONTACT_ID is None:  # create a new contact
            json_obj = self.client.get_json(
                    Config["Contacts"]["Endpoints"]["Add"]["Url"],
                    http_method=Config["Contacts"]["Endpoints"]["Add"]["Method"],
                    post_args=json.loads(self.to_json()))
            # Set initial data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)
            self.CONTACT_ID = json_obj["CONTACT_ID"]
        else:  # update existing contact
            json_obj = self.client.get_json(
                Config["Contacts"]["Endpoints"]["Update"]["Url"].format(id=force_str(self.CONTACT_ID)),
                http_method=Config["Contacts"]["Endpoints"]["Update"]["Method"],
                post_args=json.loads(self.to_json()))
            # Set new data from Insightly, includes any updates
            self.from_json(json_obj=json_obj)

    def get_contact_link(self, contact_link_id):
        """Get an contact link for this contact
        :contact_link_id: the identifier for the contact link
        :return: the contact link
        :rtype: ContactLink
        """

        contact_link = None

        for org_link in self.CONTACTLINKS:
            if org_link.CONTACT_LINK_ID == contact_link_id:
                contact_link = org_link

        return contact_link

    def add_contact_link(self, parent_contact_id, child_contact_id, relationship_id=7, details=None):
        """Add an contact link to this contact

        :parent_contact_id: Contact ID of the parent in the relationship
        :child_contact_id: Contact ID of the child in the relationship
        :relationship_id: identifier for the type of relationship, default = Parent / Subsidiary
        :details: additional details to add context
        :return: the contact link
        :rtype: ContactLink
        """
        post_args = dict(FIRST_CONTACT_ID=child_contact_id, SECOND_CONTACT_ID=parent_contact_id,
                         RELATIONSHIP_ID=relationship_id)

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["AddContactLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["AddContactLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return ContactLink.from_json(json_obj)

    def update_contact_link(self, contact_link_id, parent_contact_id=None, child_contact_id=None,
                                 relationship_id=None, details=None):
        """Update an Contact Link to this Contact
        :contact_link_id: the identifier for the contact link - note: must exist already in order to update
        :parent_contact_id: Contact ID of the parent in the relationship
        :child_contact_id: Contact ID of the child in the relationship
        :relationship_id: identifier for the type of relationship, default = Parent / Subsidiary
        :details: additional details to add context
        :return: the contact link
        :rtype: ContactLink
        """

        contact_link = self.get_contact_link(contact_link_id)

        if not contact_link:
            raise DoesNotExist("Contact Link does not exist", contact_link_id)

        post_args = dict(CONTACT_LINK_ID=contact_link_id,
                         FIRST_CONTACT_ID=child_contact_id if child_contact_id
                         else contact_link.FIRST_CONTACT_ID,
                         SECOND_CONTACT_ID=parent_contact_id if parent_contact_id
                         else contact_link.SECOND_CONTACT_ID,
                         RELATIONSHIP_ID=relationship_id if relationship_id else contact_link.RELATIONSHIP_ID)

        if details:
            post_args['DETAILS'] = details
        if not details and contact_link.DETAILS:
            post_args['DETAILS'] = contact_link.DETAILS

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["UpdateContactLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["UpdateContactLink"][
                                            "Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return ContactLink.from_json(json_obj)

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

    def add_organisation_link(self, organisation_id, role=None, details=None):
        """Add a organisation link to this organisation

        :organisation_id: Organisation ID to link to this Contact
        :role: role in this Organisation
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(CONTACT_ID=self.CONTACT_ID, ORGANISATION_ID=organisation_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_organisation_link(self, link_id=None, organisation_id=None, role=None, details=None):
        """Update a organisation link to this Contact
        :link_id: the identifier for the organisation link - note: must exist already in order to update
        :organisation_id: Organisation ID to link to this Organisation
        :role: role in this Organisation
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

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def add_opportunity_link(self, opportunity_id, role=None, details=None):
        """Add an opportunity link to this organisation

        :opportunity: Opportunity ID to link to this Contact
        :role: role in this Opportunity
        :details: additional details to add context
        :return: the link
        :rtype: Link
        """

        post_args = dict(CONTACT_ID=self.CONTACT_ID, OPPORTUNITY_ID=opportunity_id)

        if role:
            post_args['ROLE'] = role

        if details:
            post_args['DETAILS'] = details

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["AddLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["AddLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)

    def update_opportunity_link(self, link_id=None, opportunity_id=None, role=None, details=None):
        """Update a opportunity link to this Contact
        :link_id: the identifier for the opportunity link - note: must exist already in order to update
        :opportunity_id: Opportunity ID to link to this Contact
        :role: role in this Opportunity
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

        json_obj = self.client.get_json(Config["Contacts"]["Endpoints"]["UpdateLink"]["Url"]
                                        .format(id=force_str(self.CONTACT_ID)),
                                        http_method=Config["Contacts"]["Endpoints"]["UpdateLink"]["Method"],
                                        post_args=post_args)
        # self.fetch()  # update current model
        return Link.from_json(json_obj)
