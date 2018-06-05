# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import
import json
import requests
import os
import yaml
import base64
import logging

from insightly.compat import force_str
from insightly.contact import Contact
from insightly.opportunity import Opportunity, OpportunityCategory
from insightly.organisation import Organisation
from insightly.relationship import Relationship
from insightly.user import User
from insightly.exceptions import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(config_file_path) as config_file:
    Config = yaml.load(config_file)


class InsightlyClient(object):
    """ Base class for Insightly API access """

    def __init__(self, api_key, version='2.3', http_service=requests):
        """
        Constructor

        :api_key: API key found at https://crm.na1.insightly.com/users/usersettings
        """

        self.api_key = api_key
        self.version = version
        self.http_service = http_service

    def list_contacts(self, contact_filter=None):
        """
        Returns all contacts for your Insightly account

        :contact_filter: a Python dictionary of key-value pairs corresponding to query parameters defined in
            Insightly API documentation - https://api.insight.ly/v2.3/Help#!/Contacts/GetContactsBySearch

        :return: a list of Python objects representing the Insightly Contacts.
        :rtype: list of Contact

        Each Contact has the following noteworthy attributes:
            - id: the Contact's identifier
            - name: Name of the Contact
        """
        if not contact_filter:  # assume you want all
            # as of v2.2, Insightly paginates by default
            top = Config["Contacts"]["Endpoints"]["GetAll"]["DefaultQueryParameters"]["Top"]
            skip = 0

            page = self.get_json(Config["Contacts"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                 http_method=Config["Contacts"]["Endpoints"]["GetAll"]["Method"])
            json_obj = [] + page
            while len(page) > 0:
                skip += top
                page = self.get_json(Config["Contacts"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                     http_method=Config["Contacts"]["Endpoints"]["GetAll"]["Method"])
                json_obj += page
        else:
            if type(contact_filter) != dict:
                raise TypeError
            query_url = Config["Contacts"]["Endpoints"]["Search"]["Url"]
            for key, value in contact_filter.items():
                query_url += "{key}={value}".format(key=key, value=value)
            json_obj = self.get_json(query_url,
                                     http_method=Config["Contacts"]["Endpoints"]["Search"]["Method"])

        return [Contact.from_json(self, json_obj=obj) for obj in json_obj]

    def get_contact(self, contact_id):
        """Get contact

        :rtype: Contact
        """
        obj = self.get_json(Config["Contacts"]["Endpoints"]["Get"]["Url"].format(id=contact_id),
                            http_method=Config["Contacts"]["Endpoints"]["Get"]["Method"])

        return Contact.from_json(self, obj)

    def add_contact(self, first_name, last_name, owner_user_id, **kwargs):
        """Create Contact
        :param first_name: First name of the Contacts to create
        :param last_name: Last name of the Contacts to create
        :param owner_user_id: Insightly User ID of Contact owner
        :param kwargs: Optional additional fields - note: keys must match accepted fields, as defined in config.yaml
        :rtype: Contact
        """
        # minimum requirements to create
        post_args = dict(FIRST_NAME=first_name, LAST_NAME=last_name, OWNER_USER_ID=owner_user_id)  

        for key, value in kwargs.items():
            if key in Config["Contacts"]["AcceptedFields"]:
                post_args[key] = value
            else:
                logging.warn("Field not accepted, ignored - {}: {}".format(key, value))

        obj = self.get_json(Config["Contacts"]["Endpoints"]["Add"]["Url"],
                            http_method=Config["Contacts"]["Endpoints"]["Add"]["Method"],
                            post_args=post_args)
        return Contact.from_json(self, json_obj=obj)

    def delete_contact(self, contact_id):
        """Create Contact
        :param contact_id: ID of the Contacts to delete
        :rtype: Contact
        """

        obj = self.get_json(Config["Contacts"]["Endpoints"]["Delete"]["Url"].format(id=contact_id),
                            http_method=Config["Contacts"]["Endpoints"]["Delete"]["Method"])
        logging.info("Deleted Contact {id}".format(id=contact_id))
        return None

    def list_opportunities(self, opportunity_filter=None):
        """
        Returns all opportunities for your Insightly account

        :opportunity_filter: a Python dictionary of key-value pairs corresponding to query parameters defined in
            Insightly API documentation - https://api.insight.ly/v2.3/Help#!/Opportunities/GetOpportunitiesBySearch

        :return: a list of Python objects representing the Insightly Opportunities.
        :rtype: list of Opportunity

        Each Opportunity has the following noteworthy attributes:
            - id: the Opportunity's identifier
            - name: Name of the Opportunity
        """
        if not opportunity_filter:  # assume you want all
            # as of v2.2, Insightly paginates by default
            top = Config["Opportunities"]["Endpoints"]["GetAll"]["DefaultQueryParameters"]["Top"]
            skip = 0

            page = self.get_json(Config["Opportunities"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                 http_method=Config["Opportunities"]["Endpoints"]["GetAll"]["Method"])
            json_obj = [] + page
            while len(page) > 0:
                skip += top
                page = self.get_json(Config["Opportunities"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                     http_method=Config["Opportunities"]["Endpoints"]["GetAll"]["Method"])
                json_obj += page

        else:
            if type(opportunity_filter) != dict:
                raise TypeError
            query_url = Config["Opportunities"]["Endpoints"]["Search"]["Url"]
            for key, value in opportunity_filter.items():
                query_url += "{key}={value}".format(key=key, value=value)
            json_obj = self.get_json(query_url,
                                     http_method=Config["Opportunities"]["Endpoints"]["Search"]["Method"])

        return [Opportunity.from_json(self, json_obj=obj) for obj in json_obj]

    def get_opportunity(self, opportunity_id):
        """Get opportunity

        :rtype: Opportunity
        """
        obj = self.get_json(Config["Opportunities"]["Endpoints"]["Get"]["Url"].format(id=opportunity_id),
                            http_method=Config["Opportunities"]["Endpoints"]["Get"]["Method"])

        return Opportunity.from_json(self, obj)

    def add_opportunity(self, name, owner_user_id, **kwargs):
        """Create Opportunity
        :param name: Name of the Opportunities to create
        :param owner_user_id: Insightly User ID of Opportunity owner
        :param kwargs: Optional additional fields - note: keys must match accepted fields, as defined in config.yaml
        :rtype: Opportunity
        """

        # minimum requirements to create
        post_args = dict(OPPORTUNITY_NAME=name, OWNER_USER_ID=owner_user_id)

        for key, value in kwargs.items():
            if key in Config["Opportunities"]["AcceptedFields"]:
                post_args[key] = value
            else:
                logging.warn("Field not accepted, ignored - {}: {}".format(key, value))

        obj = self.get_json(Config["Opportunities"]["Endpoints"]["Add"]["Url"],
                            http_method=Config["Opportunities"]["Endpoints"]["Add"]["Method"],
                            post_args=post_args)
        return Opportunity.from_json(self, json_obj=obj)

    def delete_opportunity(self, opportunity_id):
        """Create Opportunity
        :param opportunity_id: ID of the Opportunities to delete
        :rtype: Opportunity
        """

        obj = self.get_json(Config["Opportunities"]["Endpoints"]["Delete"]["Url"].format(id=opportunity_id),
                            http_method=Config["Opportunities"]["Endpoints"]["Delete"]["Method"])
        logging.info("Deleted Opportunity {id}".format(id=opportunity_id))
        return None

    def list_opportunity_categories(self):
        """
        Returns all opportunities categories available for Insightly opportunities

        :return: a list of Python objects representing the Insightly Opportunity Categories.
        :rtype: list of OpportunityCategory

        Each Opportunity has the following noteworthy attributes:
            - CATEGORY_ID: the Opportunity Category's identifier
            - CATEGORY_NAME: Name of the Opportunity Category
        """

        top = Config["OpportunityCategories"]["Endpoints"]["GetAll"]["DefaultQueryParameters"]["Top"]
        skip = 0

        page = self.get_json(Config["OpportunityCategories"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                             http_method=Config["OpportunityCategories"]["Endpoints"]["GetAll"]["Method"])
        json_obj = [] + page
        while len(page) > 0:
            skip += top
            page = self.get_json(Config["OpportunityCategories"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                 http_method=Config["OpportunityCategories"]["Endpoints"]["GetAll"]["Method"])
            json_obj += page

        return [OpportunityCategory.from_json(json_obj=obj) for obj in json_obj]

    def list_organisations(self, organisation_filter=None):
        """
        Returns all organisations for your Insightly account

        :organisation_filter: a Python dictionary of key-value pairs corresponding to query parameters defined in
            Insightly API documentation - https://api.insight.ly/v2.3/Help#!/Organisations/GetOrganisationsBySearch

        :return: a list of Python objects representing the Insightly Organisations.
        :rtype: list of Organisation

        Each Organisation has the following noteworthy attributes:
            - id: the Organisation's identifier
            - name: Name of the Organisation
        """
        if not organisation_filter:  # assume you want all
            # as of v2.2, Insightly paginates by default
            top = Config["Organisations"]["Endpoints"]["GetAll"]["DefaultQueryParameters"]["Top"]
            skip = 0

            page = self.get_json(Config["Organisations"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                 http_method=Config["Organisations"]["Endpoints"]["GetAll"]["Method"])
            json_obj = [] + page
            while len(page) > 0:
                skip += top
                page = self.get_json(Config["Organisations"]["Endpoints"]["GetAll"]["Url"].format(skip=skip, top=top),
                                     http_method=Config["Organisations"]["Endpoints"]["GetAll"]["Method"])
                json_obj += page
        else:
            if type(organisation_filter) != dict:
                raise TypeError
            query_url = Config["Organisations"]["Endpoints"]["Search"]["Url"]
            for key, value in organisation_filter.items():
                query_url += "{key}={value}".format(key=key, value=value)
            json_obj = self.get_json(query_url,
                                     http_method=Config["Organisations"]["Endpoints"]["Search"]["Method"])

        return [Organisation.from_json(self, json_obj=obj) for obj in json_obj]

    def get_organisation(self, organisation_id):
        """Get organisation

        :rtype: Organisation
        """
        obj = self.get_json(Config["Organisations"]["Endpoints"]["Get"]["Url"].format(id=organisation_id),
                            http_method=Config["Organisations"]["Endpoints"]["Get"]["Method"])

        return Organisation.from_json(self, obj)

    def add_organisation(self, name, owner_user_id, **kwargs):
        """Create Organisation
        :param name: Name of the Organisations to create
        :param owner_user_id: Insightly User ID of Organisation owner
        :param kwargs: Optional additional fields - note: keys must match accepted fields, as defined in config.yaml
        :rtype: Organisation
        """
        post_args = dict(ORGANISATION_NAME=name, OWNER_USER_ID=owner_user_id)  # minimum requirements to create
        
        for key, value in kwargs.items():
            if key in Config["Organisations"]["AcceptedFields"]:
                post_args[key] = value
            else:
                logging.warn("Field not accepted, ignored - {}: {}".format(key, value))

        obj = self.get_json(Config["Organisations"]["Endpoints"]["Add"]["Url"],
                            http_method=Config["Organisations"]["Endpoints"]["Add"]["Method"],
                            post_args=post_args)
        return Organisation.from_json(self, json_obj=obj)

    def delete_organisation(self, organisation_id):
        """Create Organisation
        :param organisation_id: ID of the Organisations to delete
        :rtype: Organisation
        """

        obj = self.get_json(Config["Organisations"]["Endpoints"]["Delete"]["Url"].format(id=organisation_id),
                            http_method=Config["Organisations"]["Endpoints"]["Delete"]["Method"])
        logging.info("Deleted Organisation {id}".format(id=organisation_id))
        return None
    
    def list_relationships(self):
        """
        Returns all relationships for your Insightly account

        :return: a list of Python objects representing the Insightly Relationships.
        :rtype: list of Relationship

        Each Relationship has the following noteworthy attributes:
            - id: the Relationships's identifier
            - name: Name of the Relationship
        """
        json_obj = self.get_json(Config["Relationships"]["Endpoints"]["GetAll"]["Url"],
                                 http_method=Config["Relationships"]["Endpoints"]["GetAll"]["Method"])

        return [Relationship.from_json(json_obj=obj) for obj in json_obj]

    def list_users(self):
        """
        Returns all users for your Insightly account

        :return: a list of Python objects representing the Insightly Users.
        :rtype: list of User

        Each Relationship has the following noteworthy attributes:
            - USER_ID: the User's identifier
            - FIRST_NAME: First name of the User
            - LAST_NAME: Last name of the User
        """
        json_obj = self.get_json(Config["Users"]["Endpoints"]["GetAll"]["Url"],
                                 http_method=Config["Users"]["Endpoints"]["GetAll"]["Method"])

        return [User.from_json(self, json_obj=obj) for obj in json_obj]

    def get_json(
            self,
            uri_path,
            http_method='GET',
            headers=None,
            query_params=None,
            post_args=None,
            files=None):
        """ Get some JSON from Insightly """

        # TODO: Check if headers and additional request fields are needed

        # explicit values here to avoid mutable default values
        if headers is None:
            headers = dict()
        if query_params is None:
            query_params = dict()
        if post_args is None:
            post_args = dict()

        # if files specified, we don't want any data
        data = None
        if files is None:
            data = json.dumps(post_args)

        # set content type and accept headers to handle JSON
        if http_method in ("POST", "PUT", "DELETE") and not files:
            headers['Content-Type'] = 'application/json; charset=utf-8'

        # construct the full URL without query parameters
        if uri_path[0] == '/':
            uri_path = uri_path[1:]
        url = Config["BaseUrl"].format(version_number=self.version) + uri_path

        # API Key authentication
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = "Basic {}".format(base64.b64encode(bytes("{}:".format(self.api_key), 'utf-8'))
                                                     .decode())

        # perform the HTTP requests, if possible uses OAuth authentication
        response = self.http_service.request(http_method, url, params=query_params,
                                             headers=headers, data=data, files=files)

        if response.status_code == 400:
            logging.error("Failed request - {}".format(response.request))
            raise MissingOrInvalidParameter("{} at {}".format(response.text, url), response)
        if response.status_code == 401:
            logging.error("Failed request - {}".format(response.request))
            raise Unauthorized("{} at {}".format(response.text, url), response)
        if response.status_code == 403:
            logging.error("Failed request - {}".format(response.request))
            raise NoPermission("{} at {}".format(response.text, url), response)
        if response.status_code == 404:
            logging.error("Failed request - {}".format(response.request))
            raise NotFound("{} at {}".format(response.text, url), response)
        if response.status_code not in [200, 201, 202]:
            raise ResourceUnavailable("%s at %s" % (response.text, url), response)

        try:
            return response.json()
        except ValueError:  # Insightly API does not return JSON for all request types e.g. DELETE
            return response.content

    # def search(self, query, partial_match=False, models=[],
    #            board_ids=[], org_ids=[], card_ids=[]):
    #     """
    #     Search trello given a query string.
    #
    #     :param str query: A query string up to 16K characters
    #     :param bool partial_match: True means that trello will look for
    #             content that starts with any of the words in your query.
    #     :param list models: Comma-separated list of types of objects to search.
    #             This can be 'actions', 'boards', 'cards', 'members',
    #             or 'organizations'.  The default is 'all' models.
    #     :param list board_ids: Comma-separated list of boards to limit search
    #     :param org_ids: Comma-separated list of organizations to limit search
    #     :param card_ids: Comma-separated list of cards to limit search
    #
    #     :return: All objects matching the search criterial.  These can
    #         be Cards, Boards, Organizations, and Members.  The attributes
    #         of the objects in the results are minimal; the user must call
    #         the fetch method on the resulting objects to get a full set
    #         of attributes populated.
    #     :rtype list:
    #     """
    #
    #     query_params = {'query': query}
    #
    #     if partial_match:
    #         query_params['partial'] = 'true'
    #
    #     # Limit search to one or more object types
    #     if models:
    #         query_params['modelTypes'] = models
    #
    #     # Limit search to a particular subset of objects
    #     if board_ids:
    #         query_params['idBoards'] = board_ids
    #     if org_ids:
    #         query_params['idOrganizations'] = org_ids
    #     if card_ids:
    #         query_params['idCards'] = card_ids
    #
    #     # Request result fields required to instantiate class objects
    #     query_params['board_fields'] = ['name,url,desc,closed']
    #     query_params['member_fields'] = ['fullName,initials,username']
    #     query_params['organization_fields'] = ['name,url,desc']
    #
    #     json_obj = self.get_json('/search', query_params=query_params)
    #     if not json_obj:
    #         return []
    #
    #     results = []
    #     board_cache = {}
    #
    #     for board_json in json_obj.get('boards', []):
    #         # Cache board objects
    #         if board_json['id'] not in board_cache:
    #             board_cache[board_json['id']] = Organisation.from_json(
    #                 self, json_obj=board_json)
    #         results.append(board_cache[board_json['id']])
    #
    #     for card_json in json_obj.get('cards', []):
    #         # Cache board objects
    #         if card_json['idBoard'] not in board_cache:
    #             board_cache[card_json['idBoard']] = Organisation(
    #                 self, card_json['idBoard'])
    #             # Fetch the board attributes as the Organisation object created
    #             # from the card initially result lacks a URL and name.
    #             # This Organisation will be stored in Card.parent
    #             board_cache[card_json['idBoard']].fetch()
    #         results.append(Card.from_json(board_cache[card_json['idBoard']],
    #                                       card_json))
    #
    #     for member_json in json_obj.get('members', []):
    #         results.append(Member.from_json(self, member_json))
    #
    #     for org_json in json_obj.get('organizations', []):
    #         org = Organization.from_json(self, org_json)
    #         results.append(org)
    #
    #     return results

