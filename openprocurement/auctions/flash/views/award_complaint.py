# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.plugins.awarding_1_0.views.award_complaint import (
    AuctionAwardComplaintResource as BaseAuctionAwardComplaintResource
)


@opresource(name='belowThreshold:Auction Award Complaints',
            collection_path='/auctions/{auction_id}/awards/{award_id}/complaints',
            path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction award complaints")
class AuctionAwardComplaintResource(BaseAuctionAwardComplaintResource):
    pass
