# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import opresource
from openprocurement.auctions.core.views.mixins import AuctionComplaintDocumentResource


@opresource(name='belowThreshold:Auction Complaint Documents',
            collection_path='/auctions/{auction_id}/complaints/{complaint_id}/documents',
            path='/auctions/{auction_id}/complaints/{complaint_id}/documents/{document_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction complaint documents")
class AuctionComplaintDocumentResource(AuctionComplaintDocumentResource):
    pass
