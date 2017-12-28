# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_lots, test_organization
)
from openprocurement.auctions.flash.tests.blanks.complaint_blanks import (
    # AuctionComplaintResourceTest
    create_auction_complaint_invalid,
    create_auction_complaint,
    patch_auction_complaint,
    review_auction_complaint,
    get_auction_complaint,
    get_auction_complaints,
    # AuctionLotAwardComplaintResourceTest
    create_auction_lot_complaint,
    # AuctionComplaintDocumentResourceTest
    auction_complaint_document_not_found,
    create_auction_complaint_document,
    put_auction_complaint_document,
    patch_auction_complaint_document
)


class AuctionComplaintResourceTest(BaseAuctionWebTest):
    test_create_auction_complaint_invalid = snitch(create_auction_complaint_invalid)
    test_create_auction_complaint = snitch(create_auction_complaint)
    test_patch_auction_complaint = snitch(patch_auction_complaint)
    test_review_auction_complaint = snitch(review_auction_complaint)
    test_get_auction_complaint = snitch(get_auction_complaint)
    test_get_auction_complaints = snitch(get_auction_complaints)


class AuctionLotAwardComplaintResourceTest(BaseAuctionWebTest):
    initial_lots = test_lots
    test_create_auction_lot_complaint = snitch(create_auction_lot_complaint)


class AuctionComplaintDocumentResourceTest(BaseAuctionWebTest):

    def setUp(self):
        super(AuctionComplaintDocumentResourceTest, self).setUp()
        # Create complaint
        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']
    test_auction_complaint_document_not_found = snitch(auction_complaint_document_not_found)
    test_create_auction_complaint_document = snitch(create_auction_complaint_document)
    test_put_auction_complaint_document = snitch(put_auction_complaint_document)
    test_patch_auction_complaint_document = snitch(patch_auction_complaint_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionComplaintResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotAwardComplaintResourceTest))
    suite.addTest(unittest.makeSuite(AuctionComplaintDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
