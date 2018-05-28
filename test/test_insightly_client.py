#!/usr/bin/python

from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from insightly import InsightlyClient
from insightly.exceptions import *


class InsightlyClientTestCase(unittest.TestCase):
    """

    Tests for InsightlyClient API. Note these test are in order to
    preserve dependencies, as an API integration cannot be tested
    independently.

    """

    def setUp(self):
        self._insightly = InsightlyClient(os.environ['INSIGHTLY_API_KEY'])

    def test01_list_organisations(self):
        self.assertEqual(
            len(self._insightly.list_organisations()),
            int(os.environ['TEST_INSIGHTLY_TOTAL_ORGS']))

    def test02_list_contacts(self):
        self.assertEqual(
            len(self._insightly.list_contacts()),
            int(os.environ['TEST_INSIGHTLY_TOTAL_CONTACTS']))

    def test03_list_opportunities(self):
        self.assertEqual(
            len(self._insightly.list_opportunities()),
            int(os.environ['TEST_INSIGHTLY_TOTAL_OPPORTUNTIES']))

    def test04_list_users(self):
        self.assertEqual(
            len(self._insightly.list_users()),
            int(os.environ['TEST_INSIGHTLY_TOTAL_USERS']))

    def test05_list_relationships(self):
        self.assertEqual(
            len(self._insightly.list_relationships()),
            int(os.environ['TEST_INSIGHTLY_TOTAL_RELATIONSHIPS']))

    def test06_add_organisation(self):
        new_org = self._insightly.add_organisation(os.environ['TEST_NEW_INSIGHTLY_ORG'],
                                                   os.environ['TEST_INSIGHTLY_USER'])
        self.assertEqual(
            new_org.ORGANISATION_NAME,
            os.environ['TEST_NEW_INSIGHTLY_ORG']
        )
        self.assertIsNotNone(new_org.ORGANISATION_ID)

    def test07_update_organisation(self):
        update_org = [org for org in self._insightly.list_organisations()
                      if org.ORGANISATION_NAME == os.environ['TEST_NEW_INSIGHTLY_ORG']][0]

        update_org.ORGANISATION_NAME = os.environ['TEST_NEW_INSIGHTLY_ORG_UPDATE_NAME']
        update_org.save()
        check_org = self._insightly.get_organisation(update_org.ORGANISATION_ID)
        self.assertEqual(check_org.ORGANISATION_NAME,
                         os.environ['TEST_NEW_INSIGHTLY_ORG_UPDATE_NAME'])

    def test08_delete_organisation(self):
        delete_org = [org for org in self._insightly.list_organisations()
                      if org.ORGANISATION_NAME == os.environ['TEST_NEW_INSIGHTLY_ORG_UPDATE_NAME']][0]

        self._insightly.delete_organisation(delete_org.ORGANISATION_ID)

        # check that deleted organisation no longer exists
        try:
            deleted_org = self._insightly.get_organisation(delete_org.ORGANISATION_ID)
        except NotFound:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised: {}'.format(e))
        else:
            self.fail('NotFound exception not raised')

    def test09_add_contact(self):
        new_contact = self._insightly.add_contact(os.environ['TEST_NEW_INSIGHTLY_CONTACT'].split(' ')[0],
                                                  os.environ['TEST_NEW_INSIGHTLY_CONTACT'].split(' ')[1],
                                                  os.environ['TEST_INSIGHTLY_USER'])
        self.assertEqual(
            ' '.join([new_contact.FIRST_NAME, new_contact.LAST_NAME]),
            os.environ['TEST_NEW_INSIGHTLY_CONTACT']
        )
        self.assertIsNotNone(new_contact.CONTACT_ID)

    def test10_update_contact(self):
        update_contact = [contact for contact in self._insightly.list_contacts() 
                          if ' '.join([contact.FIRST_NAME, contact.LAST_NAME]) == 
                          os.environ['TEST_NEW_INSIGHTLY_CONTACT']][0]

        update_contact.FIRST_NAME = os.environ['TEST_NEW_INSIGHTLY_CONTACT_UPDATE_NAME'].split(' ')[0]
        update_contact.LAST_NAME = os.environ['TEST_NEW_INSIGHTLY_CONTACT_UPDATE_NAME'].split(' ')[1]
        update_contact.save()
        check_contact = self._insightly.get_contact(update_contact.CONTACT_ID)
        self.assertEqual(' '.join([check_contact.FIRST_NAME, check_contact.LAST_NAME]),
                         os.environ['TEST_NEW_INSIGHTLY_CONTACT_UPDATE_NAME'])

    def test11_delete_contact(self):
        delete_contact = [contact for contact in self._insightly.list_contacts() 
                          if ' '.join([contact.FIRST_NAME, contact.LAST_NAME]) == 
                          os.environ['TEST_NEW_INSIGHTLY_CONTACT_UPDATE_NAME']][0]

        self._insightly.delete_contact(delete_contact.CONTACT_ID)

        # check that deleted contact no longer exists
        try:
            deleted_contact = self._insightly.get_contact(delete_contact.CONTACT_ID)
        except NotFound:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised: {}'.format(e))
        else:
            self.fail('NotFound exception not raised')

    def test12_add_opportunity(self):
        new_opp = self._insightly.add_opportunity(os.environ['TEST_NEW_INSIGHTLY_OPP'],
                                                  os.environ['TEST_INSIGHTLY_USER'],
                                                  OPPORTUNITY_STATE=os.environ['TEST_NEW_INSIGHTLY_OPP_STATUS'])
        self.assertEqual(
            new_opp.OPPORTUNITY_NAME,
            os.environ['TEST_NEW_INSIGHTLY_OPP']
        )
        self.assertIsNotNone(new_opp.OPPORTUNITY_ID)

    def test13_update_opportunity(self):
        update_opp = [opp for opp in self._insightly.list_opportunities()
                      if opp.OPPORTUNITY_NAME == os.environ['TEST_NEW_INSIGHTLY_OPP']][0]

        update_opp.OPPORTUNITY_NAME = os.environ['TEST_NEW_INSIGHTLY_OPP_UPDATE_NAME']
        update_opp.save()
        check_opp = self._insightly.get_opportunity(update_opp.OPPORTUNITY_ID)
        self.assertEqual(check_opp.OPPORTUNITY_NAME,
                         os.environ['TEST_NEW_INSIGHTLY_OPP_UPDATE_NAME'])

    def test14_delete_opportunity(self):
        delete_opp = [opp for opp in self._insightly.list_opportunities()
                      if opp.OPPORTUNITY_NAME == os.environ['TEST_NEW_INSIGHTLY_OPP_UPDATE_NAME']][0]

        self._insightly.delete_opportunity(delete_opp.OPPORTUNITY_ID)

        # check that deleted opportunity no longer exists
        try:
            deleted_opp = self._insightly.get_opportunity(delete_opp.OPPORTUNITY_ID)
        except NotFound:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised: {}'.format(e))
        else:
            self.fail('NotFound exception not raised')


def suite():
    test_classes_to_run = [InsightlyClientTestCase]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    return unittest.TestSuite(suites_list)


if __name__ == "__main__":
    unittest.main()
