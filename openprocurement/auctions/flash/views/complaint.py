# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionComplaintResource


@opresource(name='belowThreshold:Auction Complaints',
            collection_path='/auctions/{auction_id}/complaints',
            path='/auctions/{auction_id}/complaints/{complaint_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction complaints")
class AuctionComplaintResource(AuctionComplaintResource):
    pass
