# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from insightly import InsightlyBase
from insightly.compat import force_str

import json
import jsonpickle


class OrganisationLink(InsightlyBase):
    """
    Class representing an Insightly OrganisationLink i.e. a link between two organisations. OrganisationLink attributes
    are stored as normal Python attributes.
    """

    def __init__(self, organisation_link_id=None, parent_organisation_id=None, child_organisation_id=None,
                 relationship_id=None, details=None):

        super(OrganisationLink, self).__init__()
        self.ORG_LINK_ID = organisation_link_id
        self.FIRST_ORGANISATION_ID = child_organisation_id
        self.SECOND_ORGANISATION_ID = parent_organisation_id
        self.RELATIONSHIP_ID = relationship_id
        self.DETAILS = details

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']
        if state['ORG_LINK_ID'] is None:
            del state['ORG_LINK_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the contact json object to a OrganisationLink object

        :json_obj: the contact link object
        """

        organisation_link = OrganisationLink(organisation_link_id=json_obj['ORG_LINK_ID'],
                                             parent_organisation_id=json_obj['SECOND_ORGANISATION_ID'],
                                             child_organisation_id=json_obj['FIRST_ORGANISATION_ID'],
                                             relationship_id=json_obj['RELATIONSHIP_ID'],
                                             details=json_obj['DETAILS'])

        return organisation_link

    def __repr__(self):
        return force_str(u'<OrganisationLink {}  {} --> {}>'.format(self.ORG_LINK_ID, self.SECOND_ORGANISATION_ID,
                                                                    self.FIRST_ORGANISATION_ID))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)


class ContactLink(InsightlyBase):
    """
    Class representing an Insightly ContactLink i.e. a link between two contacts. ContactLink attributes
    are stored as normal Python attributes.
    """

    def __init__(self, contact_link_id=None, parent_contact_id=None, child_contact_id=None,
                 relationship_id=None, details=None):

        super(ContactLink, self).__init__()
        self.CONTACT_LINK_ID = contact_link_id
        self.FIRST_CONTACT_ID = child_contact_id
        self.SECOND_CONTACT_ID = parent_contact_id
        self.RELATIONSHIP_ID = relationship_id
        self.DETAILS = details

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']
        if state['CONTACT_LINK_ID'] is None:
            del state['CONTACT_LINK_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the contact json object to a ContactLink object

        :json_obj: the contact link object
        """

        contact_link = ContactLink(contact_link_id=json_obj['CONTACT_LINK_ID'], 
                                   parent_contact_id=json_obj['SECOND_CONTACT_ID'],
                                   child_contact_id=json_obj['FIRST_CONTACT_ID'],
                                   relationship_id=json_obj['RELATIONSHIP_ID'],
                                   details=json_obj['DETAILS'])

        return contact_link

    def __repr__(self):
        return force_str(u'<ContactLink {}  {} --> {}>'.format(self.ORG_LINK_ID, self.SECOND_CONTACT_ID, 
                                                               self.FIRST_CONTACT_ID))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)


class OpportunityLink(InsightlyBase):
    """
    Class representing an Insightly OpportunityLink i.e. a link between two opportunitys. OpportunityLink attributes
    are stored as normal Python attributes.
    """

    def __init__(self, opportunity_link_id=None, parent_opportunity_id=None, child_opportunity_id=None,
                 relationship_id=None, details=None):

        super(OpportunityLink, self).__init__()
        self.ORG_LINK_ID = opportunity_link_id
        self.FIRST_OPPORTUNITY_ID = child_opportunity_id
        self.SECOND_OPPORTUNITY_ID = parent_opportunity_id
        self.RELATIONSHIP_ID = relationship_id
        self.DETAILS = details

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']
        if state['OPPORTUNITY_LINK_ID'] is None:
            del state['OPPORTUNITY_LINK_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the opportunity json object to a OpportunityLink object

        :json_obj: the opportunity link object
        """

        opportunity_link = OpportunityLink(opportunity_link_id=json_obj['OPPORTUNITY_LINK_ID'],
                                           parent_opportunity_id=json_obj['SECOND_OPPORTUNITY_ID'],
                                           child_opportunity_id=json_obj['FIRST_OPPORTUNITY_ID'],
                                           relationship_id=json_obj['RELATIONSHIP_ID'],
                                           details=json_obj['DETAILS'])

        return opportunity_link

    def __repr__(self):
        return force_str(u'<OpportunityLink {}  {} --> {}>'.format(self.ORG_LINK_ID, self.SECOND_OPPORTUNITY_ID, 
                                                               self.FIRST_OPPORTUNITY_ID))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)


class Link(InsightlyBase):
    """
        Class representing an Insightly Link i.e. a link between two different types of entities. Link attributes are
        stored as normal Python attributes.
    """

    def __init__(self, link_id=None, organisation_id=None, contact_id=None, opportunity_id=None,
                 second_opportunity_id=None, project_id=None, second_project_id=None,
                 role=None, details=None):

        super(Link, self).__init__()
        self.LINK_ID = link_id
        self.ORGANISATION_ID = organisation_id
        self.CONTACT_ID = contact_id
        self.OPPORTUNITY_ID = opportunity_id
        self.SECOND_OPPORTUNITY_ID = second_opportunity_id
        self.PROJECT_ID = project_id
        self.SECOND_OPPORTUNITY_ID = second_project_id
        self.ROLE = role
        self.DETAILS = details

    def __getstate__(self):
        """ Strip out any non-insightly parameters """
        state = self.__dict__.copy()
        del state['id']
        if state['LINK_ID'] is None:
            del state['LINK_ID']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_json(cls, json_obj=None):
        """
        Deserialize the link json object to a Link object

        :json_obj: the link link object
        """

        link = Link(link_id=json_obj['LINK_ID'], organisation_id=json_obj['ORGANISATION_ID'],
                    contact_id=json_obj['CONTACT_ID'], opportunity_id=json_obj['OPPORTUNITY_ID'],
                    second_opportunity_id=json_obj['SECOND_OPPORTUNITY_ID'], project_id=json_obj['PROJECT_ID'],
                    second_project_id=json_obj['SECOND_PROJECT_ID'], role=json_obj['ROLE'], details=json_obj['DETAILS'])

        return link

    def __repr__(self):
        return force_str(u'<LINK {} ORGANISATION  {}>'.format(self.LINK_ID, self.ORGANISATION_ID))

    def to_json(self):
        """ Strip out any non-insightly parameters """

        return jsonpickle.encode(self, unpicklable=False)


