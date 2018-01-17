# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest, test_lots, test_bids, test_organization
)
from openprocurement.auctions.core.tests.blanks.chronograph_blanks import (
    # AuctionSwitchAuctionResourceTest
    switch_to_auction,
    # AuctionSwitchUnsuccessfulResourceTest
    switch_to_unsuccessful,
    # AuctionComplaintSwitchResourceTest
    switch_to_pending,
    switch_to_complaint,
    # AuctionAwardComplaintSwitchResourceTest
    switch_to_pending_award,
    switch_to_complaint_award,
)
from openprocurement.auctions.flash.tests.blanks.chronograph_blanks import (
    # AuctionSwitchtenderingResourceTest
    switch_to_tendering_by_enquiryPeriod_endDate,
    switch_to_tendering_by_auctionPeriod_startDate,
    switch_to_tendering_auctionPeriod,
    # AuctionSwitchQualificationResourceTest
    switch_to_qualification,
    # AuctionAuctionPeriodResourceTest
    set_auction_period,
    reset_auction_period,
)


class AuctionSwitchtenderingResourceTest(BaseAuctionWebTest):
    test_switch_to_tendering_by_enquiryPeriod_endDate = \
        snitch(switch_to_tendering_by_enquiryPeriod_endDate)
    test_switch_to_tendering_by_auctionPeriod_startDate = \
        snitch(switch_to_tendering_by_auctionPeriod_startDate)
    test_switch_to_tendering_auctionPeriod = \
        snitch(switch_to_tendering_auctionPeriod)


class AuctionSwitchQualificationResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids[:1]
    test_switch_to_qualification = snitch(switch_to_qualification)


class AuctionSwitchAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids
    test_switch_to_auction = snitch(switch_to_auction)


class AuctionSwitchUnsuccessfulResourceTest(BaseAuctionWebTest):
    initial_status = 'active.tendering'
    test_switch_to_unsuccessful = snitch(switch_to_unsuccessful)


class AuctionLotSwitchQualificationResourceTest(AuctionSwitchQualificationResourceTest):
    initial_lots = test_lots


class AuctionLotSwitchAuctionResourceTest(AuctionSwitchAuctionResourceTest):
    initial_lots = test_lots


class AuctionLotSwitchUnsuccessfulResourceTest(AuctionSwitchUnsuccessfulResourceTest):
    initial_lots = test_lots


class AuctionAuctionPeriodResourceTest(BaseAuctionWebTest):
    initial_bids = test_bids
    test_set_auction_period = snitch(set_auction_period)
    test_reset_auction_period = snitch(reset_auction_period)


class AuctionLotAuctionPeriodResourceTest(AuctionAuctionPeriodResourceTest):
    initial_lots = test_lots


class AuctionComplaintSwitchResourceTest(BaseAuctionWebTest):
    initial_organization = test_organization

    test_switch_to_pending = snitch(switch_to_pending)
    test_switch_to_complaint = snitch(switch_to_complaint)


class AuctionLotComplaintSwitchResourceTest(AuctionComplaintSwitchResourceTest):
    initial_lots = test_lots


class AuctionAwardComplaintSwitchResourceTest(BaseAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_organization = test_organization

    def setUp(self):
        super(AuctionAwardComplaintSwitchResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']

    test_auction_award_complaint_switch_to_pending = snitch(switch_to_pending_award)
    test_auction_award_complaint_switch_to_complaint = snitch(switch_to_complaint_award)


class AuctionLotAwardComplaintSwitchResourceTest(AuctionAwardComplaintSwitchResourceTest):
    initial_lots = test_lots

    def setUp(self):
        super(AuctionAwardComplaintSwitchResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(self.auction_id), {'data': {
            'suppliers': [test_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_bids[0]['lotValues'][0]['relatedLot']
        }})
        award = response.json['data']
        self.award_id = award['id']


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionSwitchtenderingResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSwitchQualificationResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSwitchAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSwitchUnsuccessfulResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotSwitchQualificationResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotSwitchAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotSwitchUnsuccessfulResourceTest))
    suite.addTest(unittest.makeSuite(AuctionAuctionPeriodResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotAuctionPeriodResourceTest))
    suite.addTest(unittest.makeSuite(AuctionComplaintSwitchResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotComplaintSwitchResourceTest))
    suite.addTest(unittest.makeSuite(AuctionAwardComplaintSwitchResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotAwardComplaintSwitchResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
