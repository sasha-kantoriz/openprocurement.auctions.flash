# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.core.plugins.awarding_1_0.views import (
    AuctionAwardComplaintDocumentResource as BaseAuctionAwardComplaintDocumentResourse
)


@opresource(name='belowThreshold:Auction Award Complaint Documents',
            collection_path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}/documents',
            path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}/documents/{document_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction award complaint documents")
class AuctionAwardComplaintDocumentResource(BaseAuctionAwardComplaintDocumentResourse):
    pass
