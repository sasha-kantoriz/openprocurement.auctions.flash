# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionAuctionResource


@opresource(name='belowThreshold:Auction Auction',
            collection_path='/auctions/{auction_id}/auction',
            path='/auctions/{auction_id}/auction/{auction_lot_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction auction data")
class AuctionAuctionResource(AuctionAuctionResource):
    pass
