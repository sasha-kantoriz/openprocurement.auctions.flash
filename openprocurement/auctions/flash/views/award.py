# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource
)
from openprocurement.auctions.core.awarding_1_0.views import (
    AuctionAwardResource as BaseAuctionAwardResource,
)


@opresource(name='belowThreshold:Auction Awards',
            collection_path='/auctions/{auction_id}/awards',
            path='/auctions/{auction_id}/awards/{award_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction awards")
class AuctionAwardResource(BaseAuctionAwardResource):
    pass
