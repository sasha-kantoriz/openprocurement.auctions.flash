# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionLotResource


@opresource(name='belowThreshold:Auction Lots',
            collection_path='/auctions/{auction_id}/lots',
            path='/auctions/{auction_id}/lots/{lot_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction lots")
class AuctionLotResource(AuctionLotResource):
    pass
