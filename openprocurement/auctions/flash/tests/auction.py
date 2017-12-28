# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_features_auction_data,
    test_bids, test_lots, test_organization
)
from openprocurement.auctions.flash.tests.blanks.auction_blanks import (
    # AuctionAuctionResourceTest
    get_auction_auction_not_found,
    get_auction_auction,
    post_auction_auction,
    patch_auction_auction,
    post_auction_auction_document,
    # AuctionSameValueAuctionResourceTest
    post_auction_auction_not_changed,
    post_auction_auction_reversed,
    # AuctionLotAuctionResourceTest
    get_auction_auction_lot,
    post_auction_auction_lot,
    patch_auction_auction_lot,
    post_auction_auction_document_lot,
    # AuctionMultipleLotAuctionResourceTest
    get_auction_auction_2_lot,
    post_auction_auction_2_lot,
    patch_auction_auction_2_lot,
    post_auction_auction_document_2_lot,
    # AuctionFeaturesAuctionResourceTest
    get_auction_features_auction,
)


class AuctionAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    test_get_auction_auction_not_found = snitch(get_auction_auction_not_found)
    test_get_auction_auction = snitch(get_auction_auction)
    test_post_auction_auction = snitch(post_auction_auction)
    test_patch_auction_auction = snitch(patch_auction_auction)
    test_post_auction_auction_document = snitch(post_auction_auction_document)


class AuctionSameValueAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        }
        for i in range(3)
    ]
    test_post_auction_auction_not_changed = snitch(post_auction_auction_not_changed)
    test_post_auction_auction_reversed = snitch(post_auction_auction_reversed)


class AuctionLotAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    initial_lots = test_lots
    test_get_auction_auction_not_found = snitch(get_auction_auction_not_found)
    test_get_auction_auction_lots = snitch(get_auction_auction_lot)
    test_post_auction_auction_lots = snitch(post_auction_auction_lot)
    test_patch_auction_auction_lots = snitch(patch_auction_auction_lot)
    test_post_auction_auction_document_lots = snitch(post_auction_auction_document_lot)


class AuctionMultipleLotAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    initial_lots = 2 * test_lots
    test_post_auction_auction_document = snitch(get_auction_auction_not_found)
    test_get_auction_auction_multiple_lot = snitch(get_auction_auction_2_lot)
    test_post_auction_auction_multiple_lot = snitch(post_auction_auction_2_lot)
    test_patch_auction_auction_multiple_lot = snitch(patch_auction_auction_2_lot)
    test_post_auction_auction_document_multiple_lot = snitch(post_auction_auction_document_2_lot)


class AuctionFeaturesAuctionResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.auction'
    initial_bids = [
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.1,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        },
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.15,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 479,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        }
    ]
    test_get_auction_auction = snitch(get_auction_features_auction)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSameValueAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
