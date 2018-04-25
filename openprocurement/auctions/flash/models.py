# -*- coding: utf-8 -*-
from schematics.exceptions import ValidationError
from schematics.types.compound import (
    ModelType,
)
from zope.interface import implementer

from openprocurement.auctions.core.models import (
    ListType,
    ComplaintModelType,
    IAuction,
    Auction as BaseAuction,
    flashComplaint as Complaint,
    flashItem as Item,
    flashDocument as Document,
    flashCancellation as Cancellation,
    validate_items_uniq,
    validate_cav_group,
)
from openprocurement.auctions.core.plugins.awarding.v1.models import (
    Award
)
from openprocurement.auctions.core.plugins.contracting.v1.models import (
    Contract
)


class IFlashAuction(IAuction):
    """Marker interface for Flash auctions"""


@implementer(IFlashAuction)
class Auction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""

    _procedure_type = "belowThreshold"

    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the auction.
    awards = ListType(ModelType(Award), default=list())
    contracts = ListType(ModelType(Contract), default=list())
    items = ListType(ModelType(Item), required=True, min_size=1, validators=[validate_cav_group, validate_items_uniq])  # The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.
    complaints = ListType(ComplaintModelType(Complaint), default=list())
    cancellations = ListType(ModelType(Cancellation), default=list())

    def validate_tenderPeriod(self, data, period):
        if period and period.startDate and data.get('enquiryPeriod') and data.get(
                'enquiryPeriod').endDate and period.startDate < data.get('enquiryPeriod').endDate:
            raise ValidationError(u"period should begin after enquiryPeriod")


FlashAuction = Auction
