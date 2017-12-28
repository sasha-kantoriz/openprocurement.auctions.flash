# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_features_auction_data, test_organization
)
from openprocurement.auctions.flash.tests.blanks.bidder_blanks import (
    # AuctionBidderResourceTest
    create_auction_bidder_invalid,
    create_auction_bidder,
    patch_auction_bidder,
    get_auction_bidder,
    delete_auction_bidder,
    get_auction_auctioners,
    bid_Administrator_change,
    # AuctionBidderFeaturesResourceTest
    features_bidder,
    features_bidder_invalid,
    # AuctionBidderDocumentResourceTest
    auction_bidder_document_not_found,
    create_auction_bidder_document,
    put_auction_bidder_document,
    patch_auction_bidder_document,
    create_auction_bidder_document_nopending,
    # AuctionBidderDocumentWithDSResourceTest
    create_auction_bidder_document_json,
    put_auction_bidder_document_json
)


class AuctionBidderResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'

    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)
    test_patch_auction_bidder = snitch(patch_auction_bidder)
    test_get_auction_bidder = snitch(get_auction_bidder)
    test_delete_auction_bidder = snitch(delete_auction_bidder)
    test_get_auction_auctioners = snitch(get_auction_auctioners)
    test_bid_Administrator_change = snitch(bid_Administrator_change)


class AuctionBidderFeaturesResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.tendering'
    test_features_bidder = snitch(features_bidder)
    test_features_bidder_invalid = snitch(features_bidder_invalid)


class AuctionBidderDocumentResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'

    def setUp(self):
        super(AuctionBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
    test_auction_bidder_document_not_found = snitch(auction_bidder_document_not_found)
    test_create_auction_bidder_document = snitch(create_auction_bidder_document)
    test_put_auction_bidder_document = snitch(put_auction_bidder_document)
    test_patch_auction_bidder_document = snitch(patch_auction_bidder_document)
    test_create_auction_bidder_document_nopending = snitch(create_auction_bidder_document_nopending)


class AuctionBidderDocumentWithDSResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'

    def setUp(self):
        super(AuctionBidderDocumentWithDSResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
    docservice = True
    test_create_auction_bidder_document_json = snitch(create_auction_bidder_document_json)
    test_put_auction_bidder_document_json = snitch(put_auction_bidder_document_json)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionBidderResourceTest))
    suite.addTest(unittest.makeSuite(AuctionBidderFeaturesResourceTest))
    suite.addTest(unittest.makeSuite(AuctionBidderDocumentResourceTest))
    suite.addTest(unittest.makeSuite(AuctionBidderDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
