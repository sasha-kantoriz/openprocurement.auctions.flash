# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseWebTest, BaseAuctionWebTest, test_lots
)
from openprocurement.auctions.flash.tests.blanks.lot_blanks import (
    # AuctionLotResourceTest
    create_auction_lot_invalid,
    create_auction_lot,
    patch_auction_lot,
    patch_auction_currency,
    patch_auction_vat,
    get_auction_lot,
    get_auction_lots,
    delete_auction_lot,
    auction_lot_guarantee,
    # AuctionLotFeatureResourceTest
    auction_value,
    auction_features_invalid,
    # AuctionLotBidderResourceTest
    create_auction_bidder_invalid,
    patch_auction_bidder,
    # AuctionLotFeatureBidderResourceTest
    create_auction_lot_bidder_invalid,
    create_auction_bidder,
    # AuctionLotProcessTest
    auction_1lot_0bid,
    auction_1lot_1bid,
    auction_1lot_2bid,
    auction_2lot_0bid,
    auction_2lot_2can,
    auction_2lot_2bid_0com_1can_before_auction,
    auction_2lot_1bid_0com_1can,
    auction_2lot_1bid_2com_1win,
    auction_2lot_1bid_0com_0win,
    auction_2lot_1bid_1com_1win,
    auction_2lot_2bid_2com_2win,
    auction_2lot_1feature_2bid_2com_2win
)


class AuctionLotResourceTest(BaseAuctionWebTest):
    test_create_auction_lot_invalid = snitch(create_auction_lot_invalid)
    test_create_auction_lot = snitch(create_auction_lot)
    test_patch_auction_lot = snitch(patch_auction_lot)

    test_patch_auction_currency = snitch(patch_auction_currency)
    test_patch_auction_vat = snitch(patch_auction_vat)
    test_get_auction_lot = snitch(get_auction_lot)

    test_get_auction_lots = snitch(get_auction_lots)
    test_delete_auction_lot = snitch(delete_auction_lot)
    test_auction_lot_guarantee = snitch(auction_lot_guarantee)


class AuctionLotFeatureResourceTest(BaseAuctionWebTest):
    initial_lots = 2 * test_lots
    test_auction_value = snitch(auction_value)
    test_auction_features_invalid = snitch(auction_features_invalid)


class AuctionLotBidderResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_lots = test_lots
    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_patch_auction_bidder = snitch(patch_auction_bidder)


class AuctionLotFeatureBidderResourceTest(BaseAuctionWebTest):
    initial_lots = test_lots

    def setUp(self):
        super(AuctionLotFeatureBidderResourceTest, self).setUp()
        self.lot_id = self.initial_lots[0]['id']
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {"data": {
            "items": [
                {
                    'relatedLot': self.lot_id,
                    'id': '1'
                }
            ],
            "features": [
                {
                    "code": "code_item",
                    "featureOf": "item",
                    "relatedItem": "1",
                    "title": u"item feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_lot",
                    "featureOf": "lot",
                    "relatedItem": self.lot_id,
                    "title": u"lot feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_tenderer",
                    "featureOf": "tenderer",
                    "title": u"tenderer feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                }
            ]
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['items'][0]['relatedLot'], self.lot_id)
        self.set_status('active.tendering')
    test_create_auction_lot_bidder_invalid = snitch(create_auction_lot_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)


class AuctionLotProcessTest(BaseAuctionWebTest):
    setUp = BaseWebTest.setUp

    test_auction_1lot_0bid = snitch(auction_1lot_0bid)
    test_auction_1lot_1bid = snitch(auction_1lot_1bid)
    test_auction_1lot_2bid = snitch(auction_1lot_2bid)

    test_auction_2lot_0bid = snitch(auction_2lot_0bid)
    test_auction_2lot_2can = snitch(auction_2lot_2can)
    test_auction_2lot_2bid_0com_1can_before_auction = snitch(auction_2lot_2bid_0com_1can_before_auction)

    test_auction_2lot_1bid_0com_1can = snitch(auction_2lot_1bid_0com_1can)
    test_auction_2lot_1bid_2com_1win = snitch(auction_2lot_1bid_2com_1win)
    test_auction_2lot_1bid_0com_0win = snitch(auction_2lot_1bid_0com_0win)

    test_auction_2lot_1bid_1com_1win = snitch(auction_2lot_1bid_1com_1win)
    test_auction_2lot_2bid_2com_2win = snitch(auction_2lot_2bid_2com_2win)
    test_auction_2lot_1feature_2bid_2com_2win = snitch(auction_2lot_1feature_2bid_2com_2win)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionLotResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotFeatureResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotBidderResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotFeatureBidderResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotProcessTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
