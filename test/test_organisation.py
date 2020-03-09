#!/usr/bin/python
from __future__ import with_statement, print_function
from datetime import datetime
import unittest
import os
from insightly import InsightlyClient, Organisation


class InsightlyOrganisationTestCase(unittest.TestCase):
    """
    Tests for InsightlyClient API. Note these test are in order to
    preserve dependencies, as an API integration cannot be tested
    independently.
    """

    @classmethod
    def setUpClass(cls):
        cls._insightly = InsightlyClient(os.environ['INSIGHTLY_API_KEY'])
        
        for o in cls._insightly.list_organisations():
            if o.name == os.environ['TEST_EXISTING_INSIGHTLY_ORG']:
                cls._organisation = o
                break
        if not cls._organisation:
            cls.fail("Couldn't find test organisation")
        # cls._list = cls._organisation.add_list(str(datetime.now()))

    # def _add_organisation(self, name, description=None):
    #     try:
    #         org = self._insightly.add_card(name, description)
    #         self.assertIsNotNone(card, msg="card is None")
    #         self.assertIsNotNone(card.id, msg="id not provided")
    #         self.assertEqual(card.name, name)
    #         return card
    #     except Exception as e:
    #         print(str(e))
    #         self.fail("Caught Exception adding card")
    #
    # def _add_checklist(self, card, name, items=[], itemstates=None):
    #     checklist = card.add_checklist(name, items, itemstates)
    #     self.assertIsNotNone(checklist, msg="checklist is None")
    #     self.assertIsNotNone(checklist.id, msg="id not provided")
    #     self.assertEqual(checklist.name, name)
    #     return checklist
    #
    # def test_get_cards(self):
    #     # Let's ensure we have no cards in board
    #     for card in self._organisation.get_cards():
    #         card.delete()
    #
    #     nb_cards = 3
    #     names = ["Card #" + str(i) for i in range(nb_cards)]
    #     for i in range(nb_cards):
    #         self._add_organisation(names[i])
    #     cards = self._organisation.get_cards()
    #     self.assertEqual(len(cards), nb_cards)
    #     self.assertEqual(len(cards), len(self._organisation.open_cards()))
    #
    #     for card in cards:
    #         self.assertTrue(card.name in names, 'Unexpected card found')
    #
    #     self.assertIsInstance(self._organisation.all_cards(), list)
    #     self.assertIsInstance(self._organisation.open_cards(), list)
    #     self.assertIsInstance(self._organisation.closed_cards(), list)
    #
    # def test_fetch_action_limit(self):
    #     card = self._add_organisation('For action limit testing')
    #     card.set_closed(True)
    #     self._organisation.fetch_actions(action_filter='all', action_limit=2)
    #     actions = sorted(self._organisation.actions,key=lambda act: act['date'], reverse=True)
    #     self.assertEqual(len(actions), 2)
    #     self.assertEqual(actions[0]['type'], 'updateCard')
    #     self.assertFalse(actions[0]['data']['old']['closed'])
    #     self.assertEqual(actions[1]['type'], 'createCard')
    #
    # def test_fetch_action_filter(self):
    #     card = self._add_organisation('For action filter testing')
    #     card.set_closed(True) # This action will be skipped by filter
    #     self._organisation.fetch_actions(action_filter='createCard', action_limit=1)
    #     actions = self._organisation.actions
    #     self.assertEqual(len(actions), 1)
    #     self.assertEqual(actions[0]['type'], 'createCard')
    #
    # def test_delete_cards(self):
    #     self._add_organisation("card to be deleted")
    #     cards = self._organisation.open_cards()
    #     nb_open_cards = len(cards)
    #     for card in cards:
    #         card.delete()
    #     self._organisation.fetch_actions(action_filter='all', action_limit=nb_open_cards)
    #     self.assertEqual(len(self._organisation.actions), nb_open_cards)
    #     for action in self._organisation.actions:
    #         self.assertEqual(action['type'], 'deleteCard')
    #
    # def test_close_cards(self):
    #     nb_closed_cards = len(self._organisation.closed_cards())
    #     self._add_organisation("card to be closed")
    #     cards = self._organisation.open_cards()
    #     nb_open_cards = len(cards)
    #     for card in cards:
    #         card.set_closed(True)
    #     cards_after = self._organisation.closed_cards()
    #     nb_cards_after = len(cards_after)
    #     self.assertEqual(nb_cards_after, nb_closed_cards + nb_open_cards)
    #
    #
    # def test_all_cards_reachable(self):
    #     if not len(self._organisation.open_cards()):
    #         self._add_organisation("an open card")
    #     if not len(self._organisation.closed_cards()):
    #         card = self._add_organisation("card to be closed")
    #         card.set_closed(True)
    #     self.assertEqual(len(self._organisation.all_cards()),
    #                       len(self._organisation.open_cards()) + len(self._organisation.closed_cards()))
    #
    # def test70_all_members(self):
    #     self.assertTrue(len(self._organisation.all_members()) > 0)
    #
    # def test71_normal_members(self):
    #     self.assertTrue(len(self._organisation.normal_members()) >= 0)
    #
    # def test72_admin_members(self):
    #     self.assertTrue(len(self._organisation.admin_members()) > 0)
    #
    # def test73_owner_members(self):
    #     members = self._organisation.owner_members()
    #     self.assertTrue(len(members) > 0)
    #     member = members[0].fetch()
    #     self.assertNotEqual(member.status, None)
    #     self.assertNotEqual(member.id, None)
    #     self.assertNotEqual(member.bio, None)
    #     self.assertNotEqual(member.url, None)
    #     self.assertNotEqual(member.username, None)
    #     self.assertNotEqual(member.full_name, None)
    #     self.assertNotEqual(member.initials, None)
    #     member2 = self._insightly.get_member(member.id)
    #     self.assertEqual(member.username, member2.username)
    #
    # def test90_get_organisation(self):
    #     board = self._insightly.get_organisation(self._organisation.id)
    #     self.assertEqual(self._organisation.name, board.name)
    #
    # def test100_add_organisation(self):
    #     test_organisation = self._insightly.add_organisation("test_create_organisation")
    #     test_list = test_organisation.add_list("test_list")
    #     test_list.add_card("test_card")
    #     open_organisations = self._insightly.list_organisations(board_filter="open")
    #     self.assertEqual(len([x for x in open_organisations if x.name == "test_create_organisation"]), 1)
    #
    # def test110_copy_organisation(self):
    #     boards = self._insightly.list_organisations(board_filter="open")
    #     source_organisation = next( x for x in boards if x.name == "test_create_organisation")
    #     self._insightly.add_organisation("copied_organisation", source_organisation=source_organisation)
    #     listed_organisations = self._insightly.list_organisations(board_filter="open")
    #     copied_organisation = next(iter([x for x in listed_organisations if x.name == "copied_organisation"]), None)
    #     self.assertIsNotNone(copied_organisation)
    #     open_lists = copied_organisation.open_lists()
    #     self.assertEqual(len(open_lists), 4) # default lists plus mine
    #     test_list = open_lists[0]
    #     self.assertEqual(len(test_list.list_cards()), 1)
    #     test_card = next ( iter([ x for x in test_list.list_cards() if x.name == "test_card"]), None )
    #     self.assertIsNotNone(test_card)
    #
    # def test120_close_organisation(self):
    #     boards = self._insightly.list_organisations(board_filter="open")
    #     open_count = len(boards)
    #     test_create_organisation = next( x for x in boards if x.name == "test_create_organisation") # type: Organisation
    #     copied_organisation = next( x for x in boards if x.name == "copied_organisation") # type: Organisation
    #     test_create_organisation.close()
    #     copied_organisation.close()
    #     still_open_organisations = self._insightly.list_organisations(board_filter="open")
    #     still_open_count = len(still_open_organisations)
    #     self.assertEqual(still_open_count, open_count - 2)
    #
    # def test130_get_checklists_organisation(self):
    #     chklists = self._organisation.get_checklists(cards = 'open')
    #     for chklst in chklists:
    #         chklst.delete()
    #     card = self._add_organisation('For checklist testing')
    #     chklist = self._add_checklist(card, "Test Checklist", items=["item1","item2"], itemstates = [True, False])
    #     new_chklists = self._organisation.get_checklists()
    #     test_chk = new_chklists[0]
    #     self.assertEqual(test_chk.name, "Test Checklist")
    #     self.assertEqual(test_chk.trello_card, card.id)
    #     self.assertEqual(len(new_chklists), 1)
    #     i1 = test_chk.items[0]
    #     i2 = test_chk.items[1]
    #     self.assertEqual(len(test_chk.items), 2)
    #     self.assertEqual(i1['name'], "item1")
    #     self.assertEqual(i1['state'], "complete")
    #     self.assertEqual(i2['name'], "item2")
    #     self.assertEqual(i2['state'], "incomplete")
    #
    # def test_last_activity(self):
    #     self.assertIsInstance(self._organisation.date_last_activity, datetime)
    #     self.assertIsInstance(self._organisation.get_last_activity(), datetime)

def suite():
    # tests = ['test01_list_organisations', 'test10_organisation_attrs', 'test20_add_organisation']
    # return unittest.TestSuite(map(InsightlyOrganisationTestCase, tests))
    return unittest.TestLoader().loadTestsFromTestCase(InsightlyOrganisationTestCase)

if __name__ == "__main__":
    unittest.main()
