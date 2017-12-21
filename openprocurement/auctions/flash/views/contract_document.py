# -*- coding: utf-8 -*-
from openprocurement.auctions.core.contracting.flash.views.\
    contract_document import BaseAuctionAwardContractDocumentResource
from openprocurement.auctions.core.utils import opresource


@opresource(name='belowThreshold:Auction Contract Documents',
            collection_path='/auctions/{auction_id}/contracts/{contract_id}/documents',
            path='/auctions/{auction_id}/contracts/{contract_id}/documents/{document_id}',
            auctionsprocurementMethodType="belowThreshold",
            description="Auction contract documents")
class AuctionAwardContractDocumentResource(
    BaseAuctionAwardContractDocumentResource
):
    pass
