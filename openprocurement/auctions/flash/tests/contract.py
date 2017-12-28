# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_auction_data, test_bids, test_lots, test_organization
)
from openprocurement.auctions.flash.tests.blanks.contract_blanks import (
    # AuctionContractResourceTest
    create_auction_contract_invalid,
    create_auction_contract,
    create_auction_contract_in_complete_status,
    patch_auction_contract,
    get_auction_contract,
    get_auction_contracts,
    # Auction2LotContractResourceTest
    patch_auction_2_lot_contract,
    # AuctionContractDocumentResourceTest
    auction_contract_document_not_found,
    create_auction_contract_document,
    put_auction_contract_document,
    patch_auction_contract_document,
    # Auction2LotContractDocumentResourceTest
    create_auction_2_lot_contract_document,
    put_auction_2_lot_contract_document,
    patch_auction_2_lot_contract_document
)


class AuctionContractResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id'], 'value': test_auction_data["value"], 'items': test_auction_data["items"]}})
        award = response.json['data']
        self.award_id = award['id']
        self.award_value = award['value']
        self.award_suppliers = award['suppliers']
        self.award_items = award['items']
        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
    test_create_auction_contract_invalid = snitch(create_auction_contract_invalid)
    test_create_auction_contract = snitch(create_auction_contract)
    test_create_auction_contract_in_complete_status = snitch(create_auction_contract_in_complete_status)
    test_patch_auction_contract = snitch(patch_auction_contract)
    test_get_auction_contract = snitch(get_auction_contract)
    test_get_auction_contracts = snitch(get_auction_contracts)


class Auction2LotContractResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotContractResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(self.auction_id), {'data': {
            'suppliers': [test_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']
        self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
    test_patch_auction_lots_contract = snitch(patch_auction_2_lot_contract)


class AuctionContractDocumentResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionContractDocumentResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id),
            {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']
        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id),
                                       {"data": {"status": "active"}})
        # Create contract for award
        response = self.app.post_json('/auctions/{}/contracts'.format(self.auction_id), {
            'data': {'title': 'contract title', 'description': 'contract description', 'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
    test_auction_contract_document_not_found = snitch(auction_contract_document_not_found)
    test_create_auction_contract_document = snitch(create_auction_contract_document)
    test_put_auction_contract_document = snitch(put_auction_contract_document)
    test_patch_auction_contract_document = snitch(patch_auction_contract_document)


class Auction2LotContractDocumentResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotContractDocumentResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(self.auction_id), {'data': {
            'suppliers': [test_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']
        self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
        # Create contract for award
        response = self.app.post_json('/auctions/{}/contracts'.format(self.auction_id), {'data': {'title': 'contract title', 'description': 'contract description', 'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
    test_create_auction_lots_contract_document = snitch(create_auction_2_lot_contract_document)
    test_put_auction_lots_contract_document = snitch(put_auction_2_lot_contract_document)
    test_patch_auction_lots_contract_document = snitch(patch_auction_2_lot_contract_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionContractResourceTest))
    suite.addTest(unittest.makeSuite(Auction2LotContractResourceTest))
    suite.addTest(unittest.makeSuite(AuctionContractDocumentResourceTest))
    suite.addTest(unittest.makeSuite(Auction2LotContractDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
