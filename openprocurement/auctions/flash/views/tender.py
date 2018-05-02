# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionResource


@opresource(name='belowThreshold:Auction',
            path='/auctions/{auction_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Open Contracting compatible data exchange format. See http://ocds.open-contracting.org/standard/r/master/#auction for more info")
class AuctionResource(AuctionResource):
    pass
