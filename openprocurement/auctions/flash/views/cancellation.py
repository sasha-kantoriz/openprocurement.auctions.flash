# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionCancellationResource


@opresource(name='belowThreshold:Auction Cancellations',
            collection_path='/auctions/{auction_id}/cancellations',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction cancellations")
class AuctionCancellationResource(AuctionCancellationResource):
    pass
