# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionDocumentResource


@opresource(name='belowThreshold:Auction Documents',
            collection_path='/auctions/{auction_id}/documents',
            path='/auctions/{auction_id}/documents/{document_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction related binary files (PDFs, etc.)")
class AuctionDocumentResource(AuctionDocumentResource):
    pass
