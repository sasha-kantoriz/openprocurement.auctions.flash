# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionQuestionResource


@opresource(name='belowThreshold:Auction Questions',
            collection_path='/auctions/{auction_id}/questions',
            path='/auctions/{auction_id}/questions/{question_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction questions")
class AuctionQuestionResource(AuctionQuestionResource):
    pass
