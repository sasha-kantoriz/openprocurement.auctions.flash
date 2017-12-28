# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import BaseWebTest, BaseAuctionWebTest
from openprocurement.auctions.flash.tests.blanks.tender_blanks import (
    # AuctionTest
    simple_add_auction,
    create_role,
    edit_role,
    # AuctionResourceTest
    auction_Administrator_change,
    guarantee, auction_not_found,
    dateModified_auction,
    patch_auction,
    patch_tender_jsonpatch,
    auction_features,
    get_auction,
    auction_features_invalid,
    create_auction,
    create_auction_draft,
    create_auction_generated,
    create_auction_invalid,
    listing_draft, listing_changes,
    listing,
    empty_listing,
    # AuctionProcessTest
    invalid_auction_conditions,
    one_valid_bid_auction,
    one_invalid_bid_auction,
    first_bid_auction
)


class AuctionTest(BaseWebTest):
    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class AuctionResourceTest(BaseWebTest):
    test_empty_listing = snitch(empty_listing)
    test_listing = snitch(listing)
    test_listing_changes = snitch(listing_changes)
    test_listing_draft = snitch(listing_draft)
    test_create_auction_invalid = snitch(create_auction_invalid)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction_draft = snitch(create_auction_draft)
    test_create_auction = snitch(create_auction)
    test_get_auction = snitch(get_auction)
    test_auction_features_invalid = snitch(auction_features_invalid)
    test_auction_features = snitch(auction_features)
    test_patch_tender_jsonpatch = snitch(patch_tender_jsonpatch)
    test_patch_auction = snitch(patch_auction)
    test_dateModified_auction = snitch(dateModified_auction)
    test_auction_not_found = snitch(auction_not_found)
    test_guarantee = snitch(guarantee)
    test_auction_Administrator_change = snitch(auction_Administrator_change)


class AuctionProcessTest(BaseAuctionWebTest):
    setUp = BaseWebTest.setUp
    test_invalid_auction_conditions = snitch(invalid_auction_conditions)
    test_one_valid_bid_auction = snitch(one_valid_bid_auction)
    test_one_invalid_bid_auction = snitch(one_invalid_bid_auction)
    test_first_bid_auction = snitch(first_bid_auction)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionTest))
    suite.addTest(unittest.makeSuite(AuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
