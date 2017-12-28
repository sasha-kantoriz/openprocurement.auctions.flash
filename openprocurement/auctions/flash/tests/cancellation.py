# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_lots, test_bids
)
from openprocurement.auctions.flash.tests.blanks.cancellation_blanks import (
    # AuctionCancellationResourceTest
    create_auction_cancellation_invalid,
    create_auction_cancellation,
    patch_auction_cancellation,
    get_auction_cancellation,
    get_auction_cancellations,
    # AuctionLotCancellationResourceTest
    create_auction_lot_cancellation,
    patch_auction_lot_cancellation,
    # AuctionLotsCancellationResourceTest
    create_auction_2_lot_cancellation,
    patch_auction_2_lot_cancellation,
    # AuctionCancellationDocumentResourceTest
    auction_cancellation_document_not_found,
    create_auction_cancellation_document,
    put_auction_cancellation_document,
    patch_auction_cancellation_document
)


class AuctionCancellationResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    test_create_auction_cancellation_invalid = snitch(create_auction_cancellation_invalid)
    test_create_auction_cancellation = snitch(create_auction_cancellation)
    test_patch_auction_cancellation = snitch(patch_auction_cancellation)
    test_get_auction_cancellation = snitch(get_auction_cancellation)
    test_get_auction_cancellations = snitch(get_auction_cancellations)


class AuctionLotCancellationResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_lots = test_lots
    initial_bids = test_bids
    test_create_auction_lot_cancellation = snitch(create_auction_lot_cancellation)
    test_patch_auction_lot_cancellation = snitch(patch_auction_lot_cancellation)


class AuctionLotsCancellationResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_lots = 2 * test_lots
    initial_bids = test_bids
    test_create_auction_lots_cancellation = snitch(create_auction_2_lot_cancellation)
    test_patch_auction_lots_cancellation = snitch(patch_auction_2_lot_cancellation)


class AuctionCancellationDocumentResourceTest(BaseAuctionWebTest):

    def setUp(self):
        super(AuctionCancellationDocumentResourceTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations'.format(
            self.auction_id), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']
    test_auction_cancellation_document_not_found = snitch(auction_cancellation_document_not_found)
    test_create_auction_cancellation_document = snitch(create_auction_cancellation_document)
    test_put_auction_cancellation_document = snitch(put_auction_cancellation_document)
    test_patch_auction_cancellation_document = snitch(patch_auction_cancellation_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionCancellationResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotCancellationResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotsCancellationResourceTest))
    suite.addTest(unittest.makeSuite(AuctionCancellationDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
