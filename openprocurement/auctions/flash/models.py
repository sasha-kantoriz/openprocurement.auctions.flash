# -*- coding: utf-8 -*-
from datetime import (
    datetime,
    timedelta,
    time
)
from pyramid.security import Allow
from couchdb_schematics.document import SchematicsDocument
from schematics.exceptions import ValidationError
from schematics.transforms import (
    whitelist,
    blacklist
)
from schematics.types import (
    StringType,
    FloatType,
    IntType,
    URLType,
    BooleanType,
    BaseType,
    MD5Type
)
from schematics.types.compound import (
    ModelType,
    DictType,
)
from schematics.types.serializable import serializable
from uuid import uuid4
from barbecue import vnmax
from zope.interface import implementer
from openprocurement.api.models import (
    IsoDateTimeType,
    ListType,
    Model,
    Value,
    PeriodEndRequired,
    SANDBOX_MODE,
    Organization,
    Parameter,
    validate_parameters_uniq,
    LotValue,
    Bid,
    Revision,
    Question,
    Cancellation,
    Feature,
    Lot,
    schematics_embedded_role,
    schematics_default_role,
    validate_features_uniq,
    validate_items_uniq,
    validate_lots_uniq,
    Period,
    TZ,
    get_now,
    ComplaintModelType
)
from openprocurement.auctions.core.models import (
    IAuction,
    get_auction,
    flashComplaint as Complaint,
    flashItem as Item,
    Document
)
from openprocurement.auctions.core.plugins.awarding_1_0.models import (
    Award
)
from openprocurement.auctions.core.plugins.awarding_1_0.utils import (
    next_check_awarding
)
from openprocurement.auctions.core.plugins.contracting.flash.models import (
    Contract
)


STAND_STILL_TIME = timedelta(days=2)
COMPLAINT_STAND_STILL_TIME = timedelta(days=3)
BIDDER_TIME = timedelta(minutes=3 * 3)
SERVICE_TIME = timedelta(minutes=5 + 3 + 3)
AUCTION_STAND_STILL_TIME = timedelta(minutes=15)


class Guarantee(Model):
    amount = FloatType(required=True, min_value=0)  # Amount as a number.
    currency = StringType(required=True, default=u'UAH', max_length=3, min_length=3)  # The currency in 3-letter ISO 4217 format.


class AuctionPeriodEndRequired(PeriodEndRequired):

    def validate_startDate(self, data, period):
        if period and data.get('endDate') and data.get('endDate') < period:
            raise ValidationError(u"period should begin before its end")


def calc_auction_end_time(bids, start):
    return start + bids * BIDDER_TIME + SERVICE_TIME + AUCTION_STAND_STILL_TIME


def rounding_shouldStartAfter(start_after, auction, use_from=datetime(2016, 6, 1, tzinfo=TZ)):
    if (auction.enquiryPeriod and auction.enquiryPeriod.startDate or get_now()) > use_from and not (SANDBOX_MODE and auction.submissionMethodDetails and u'quick' in auction.submissionMethodDetails):
        midnigth = datetime.combine(start_after.date(), time(0, tzinfo=start_after.tzinfo))
        if start_after > midnigth:
            start_after = midnigth + timedelta(1)
    return start_after


class AuctionAuctionPeriod(Period):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if auction.lots or auction.status not in ['active.tendering', 'active.auction']:
            return
        if self.startDate and get_now() > calc_auction_end_time(auction.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        else:
            start_after = auction.tenderPeriod.endDate
        return rounding_shouldStartAfter(start_after, auction).isoformat()


class LotAuctionPeriod(Period):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = get_auction(self)
        lot = self.__parent__
        if auction.status not in ['active.tendering', 'active.auction'] or lot.status != 'active':
            return
        if auction.status == 'active.auction' and lot.numberOfBids < 2:
            return
        if self.startDate and get_now() > calc_auction_end_time(lot.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        else:
            start_after = auction.tenderPeriod.endDate
        return rounding_shouldStartAfter(start_after, auction).isoformat()


class Unit(Model):
    """Description of the unit which the good comes in e.g. hours, kilograms. Made up of a unit name, and the value of a single unit."""

    name = StringType()
    name_en = StringType()
    name_ru = StringType()
    value = ModelType(Value)
    code = StringType(required=True)


class Address(Model):

    streetAddress = StringType()
    locality = StringType()
    region = StringType()
    postalCode = StringType()
    countryName = StringType(required=True)
    countryName_en = StringType()
    countryName_ru = StringType()


class Location(Model):

    latitude = BaseType(required=True)
    longitude = BaseType(required=True)
    elevation = BaseType()


class ProcuringEntity(Organization):
    """An organization."""
    class Options:
        roles = {
            'embedded': schematics_embedded_role,
            'view': schematics_default_role,
            'edit_active.enquiries': schematics_default_role + blacklist("kind"),
            'edit_active.tendering': schematics_default_role + blacklist("kind"),
        }

    kind = StringType(choices=['general', 'special', 'defense', 'other'])


class Parameter(Parameter):

    def validate_code(self, data, code):
        if isinstance(data['__parent__'], Model) and code not in [i.code for i in (get_auction(data['__parent__']).features or [])]:
            raise ValidationError(u"code should be one of feature code.")

    def validate_value(self, data, value):
        if isinstance(data['__parent__'], Model):
            auction = get_auction(data['__parent__'])
            codes = dict([(i.code, [x.value for x in i.enum]) for i in (auction.features or [])])
            if data['code'] in codes and value not in codes[data['code']]:
                raise ValidationError(u"value should be one of feature value.")


class LotValue(LotValue):

    def validate_value(self, data, value):
        if value and isinstance(data['__parent__'], Model) and data['relatedLot']:
            lots = [i for i in get_auction(data['__parent__']).lots if i.id == data['relatedLot']]
            if not lots:
                return
            lot = lots[0]
            if lot.value.amount > value.amount:
                raise ValidationError(u"value of bid should be greater than value of lot")
            if lot.get('value').currency != value.currency:
                raise ValidationError(u"currency of bid should be identical to currency of value of lot")
            if lot.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                raise ValidationError(u"valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of lot")

    def validate_relatedLot(self, data, relatedLot):
        if isinstance(data['__parent__'], Model) and relatedLot not in [i.id for i in get_auction(data['__parent__']).lots]:
            raise ValidationError(u"relatedLot should be one of lots")


view_bid_role = (blacklist('owner_token') + schematics_default_role)
Administrator_bid_role = whitelist('tenderers')


class Bid(Bid):

    class Options:
        roles = {
            'embedded': view_bid_role,
            'view': view_bid_role,
            'auction_view': whitelist('value', 'lotValues', 'id', 'date', 'parameters', 'participationUrl', 'owner'),
            'active.qualification': view_bid_role,
            'active.awarded': view_bid_role,
            'complete': view_bid_role,
            'unsuccessful': view_bid_role,
            'cancelled': view_bid_role,
        }

    tenderers = ListType(ModelType(Organization), required=True, min_size=1, max_size=1)
    parameters = ListType(ModelType(Parameter), default=list(), validators=[validate_parameters_uniq])
    lotValues = ListType(ModelType(LotValue), default=list())
    documents = ListType(ModelType(Document), default=list())

    value = ModelType(Value)
    participationUrl = URLType()
    owner_token = StringType()
    owner = StringType()

    def validate_participationUrl(self, data, url):
        if url and isinstance(data['__parent__'], Model) and get_auction(data['__parent__']).lots:
            raise ValidationError(u"url should be posted for each lot of bid")

    def validate_lotValues(self, data, values):
        if isinstance(data['__parent__'], Model):
            auction = data['__parent__']
            if auction.lots and not values:
                raise ValidationError(u'This field is required.')

    def validate_value(self, data, value):
        if isinstance(data['__parent__'], Model):
            auction = data['__parent__']
            if auction.lots:
                if value:
                    raise ValidationError(u"value should be posted for each lot of bid")
            else:
                if not value:
                    raise ValidationError(u'This field is required.')
                if auction.value.amount > value.amount:
                    raise ValidationError(u"value of bid should be greater than value of auction")
                if auction.get('value').currency != value.currency:
                    raise ValidationError(u"currency of bid should be identical to currency of value of auction")
                if auction.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                    raise ValidationError(u"valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of auction")

    def validate_parameters(self, data, parameters):
        if isinstance(data['__parent__'], Model):
            auction = data['__parent__']
            if auction.lots:
                lots = [i.relatedLot for i in data['lotValues']]
                items = [i.id for i in auction.items if i.relatedLot in lots]
                codes = dict([
                    (i.code, [x.value for x in i.enum])
                    for i in (auction.features or [])
                    if i.featureOf == 'tenderer' or i.featureOf == 'lot' and i.relatedItem in lots or i.featureOf == 'item' and i.relatedItem in items
                ])
                if set([i['code'] for i in parameters]) != set(codes):
                    raise ValidationError(u"All features parameters is required.")
            elif not parameters and auction.features:
                raise ValidationError(u'This field is required.')
            elif set([i['code'] for i in parameters]) != set([i.code for i in (auction.features or [])]):
                raise ValidationError(u"All features parameters is required.")


class Question(Question):

    def validate_relatedItem(self, data, relatedItem):
        if not relatedItem and data.get('questionOf') in ['item', 'lot']:
            raise ValidationError(u'This field is required.')
        if relatedItem and isinstance(data['__parent__'], Model):
            auction = get_auction(data['__parent__'])
            if data.get('questionOf') == 'lot' and relatedItem not in [i.id for i in auction.lots]:
                raise ValidationError(u"relatedItem should be one of lots")
            if data.get('questionOf') == 'item' and relatedItem not in [i.id for i in auction.items]:
                raise ValidationError(u"relatedItem should be one of items")


class Cancellation(Cancellation):

    documents = ListType(ModelType(Document), default=list())


class FeatureValue(Model):

    value = FloatType(required=True, min_value=0.0, max_value=0.3)
    title = StringType(required=True, min_length=1)
    title_en = StringType()
    title_ru = StringType()
    description = StringType()
    description_en = StringType()
    description_ru = StringType()


default_lot_role = (blacklist('numberOfBids') + schematics_default_role)
embedded_lot_role = (blacklist('numberOfBids') + schematics_embedded_role)


class Lot(Lot):
    def validate_minimalStep(self, data, value):
        if value and value.amount and data.get('value'):
            if data.get('value').amount < value.amount:
                raise ValidationError(u"value should be less than value of lot")
    auctionPeriod = ModelType(LotAuctionPeriod, default={})

def validate_cav_group(items, *args):
    if items and len(set([i.classification.id[:3] for i in items])) != 1:
        raise ValidationError(u"CAV group of items be identical")


plain_role = (blacklist('_attachments', 'revisions', 'dateModified') + schematics_embedded_role)
create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'auctionID', 'bids', 'documents', 'awards', 'questions', 'complaints', 'auctionUrl', 'status', 'auctionPeriod', 'awardPeriod', 'procurementMethod', 'awardCriteria', 'submissionMethod', 'cancellations', 'numberOfBidders', 'contracts') + schematics_embedded_role)
draft_role = whitelist('status')
edit_role = (blacklist('status', 'procurementMethodType', 'lots', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'auctionID', 'bids', 'documents', 'awards', 'questions', 'complaints', 'auctionUrl', 'auctionPeriod', 'awardPeriod', 'procurementMethod', 'awardCriteria', 'submissionMethod', 'mode', 'cancellations', 'numberOfBidders', 'contracts') + schematics_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + schematics_embedded_role)
listing_role = whitelist('dateModified', 'doc_id')
auction_view_role = whitelist('auctionID', 'dateModified', 'bids', 'auctionPeriod', 'minimalStep', 'auctionUrl', 'features', 'lots', 'items', 'procurementMethodType')
auction_post_role = whitelist('bids')
auction_patch_role = whitelist('auctionUrl', 'bids', 'lots')
enquiries_role = (blacklist('owner_token', '_attachments', 'revisions', 'bids', 'numberOfBids') + schematics_embedded_role)
auction_role = (blacklist('owner_token', '_attachments', 'revisions', 'bids', 'numberOfBids') + schematics_embedded_role)
#chronograph_role = whitelist('status', 'enquiryPeriod', 'tenderPeriod', 'auctionPeriod', 'awardPeriod', 'lots')
chronograph_role = whitelist('auctionPeriod', 'lots', 'next_check')
chronograph_view_role = whitelist('status', 'enquiryPeriod', 'tenderPeriod', 'auctionPeriod', 'awardPeriod', 'awards', 'lots', 'doc_id', 'submissionMethodDetails', 'mode', 'numberOfBids', 'complaints', 'procurementMethodType')
Administrator_role = whitelist('status', 'mode', 'procuringEntity','auctionPeriod', 'lots')


@implementer(IAuction)
class Auction(SchematicsDocument, Model):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    class Options:
        roles = {
            'plain': plain_role,
            'create': create_role,
            'edit': edit_role,
            'edit_draft': draft_role,
            'edit_active.enquiries': edit_role,
            'edit_active.tendering': whitelist(),
            'edit_active.auction': whitelist(),
            'edit_active.qualification': whitelist(),
            'edit_active.awarded': whitelist(),
            'edit_complete': whitelist(),
            'edit_unsuccessful': whitelist(),
            'edit_cancelled': whitelist(),
            'view': view_role,
            'listing': listing_role,
            'auction_view': auction_view_role,
            'auction_post': auction_post_role,
            'auction_patch': auction_patch_role,
            'draft': enquiries_role,
            'active.enquiries': enquiries_role,
            'active.tendering': enquiries_role,
            'active.auction': auction_role,
            'active.qualification': view_role,
            'active.awarded': view_role,
            'complete': view_role,
            'unsuccessful': view_role,
            'cancelled': view_role,
            'chronograph': chronograph_role,
            'chronograph_view': chronograph_view_role,
            'Administrator': Administrator_role,
            'default': schematics_default_role,
            'contracting': whitelist('doc_id', 'owner'),
        }

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'auction_owner')])
        for i in self.bids:
            roles['{}_{}'.format(i.owner, i.owner_token)] = 'bid_owner'
        return roles

    title = StringType(required=True)
    title_en = StringType()
    title_ru = StringType()
    description = StringType()
    description_en = StringType()
    description_ru = StringType()
    date = IsoDateTimeType()
    auctionID = StringType()  # AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    items = ListType(ModelType(Item), required=True, min_size=1, validators=[validate_cav_group, validate_items_uniq])  # The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.
    value = ModelType(Value, required=True)  # The total estimated value of the procurement.
    procurementMethod = StringType(choices=['open', 'selective', 'limited'], default='open')  # Specify tendering method as per GPA definitions of Open, Selective, Limited (http://www.wto.org/english/docs_e/legal_e/rev-gpr-94_01_e.htm)
    procurementMethodRationale = StringType()  # Justification of procurement method, especially in the case of Limited tendering.
    procurementMethodRationale_en = StringType()
    procurementMethodRationale_ru = StringType()
    awardCriteria = StringType(choices=['highestCost', 'bestProposal', 'bestValueToGovernment', 'singleBidOnly'], default='highestCost')  # Specify the selection criteria, by lowest cost,
    awardCriteriaDetails = StringType()  # Any detailed or further information on the selection criteria.
    awardCriteriaDetails_en = StringType()
    awardCriteriaDetails_ru = StringType()
    submissionMethod = StringType(choices=['electronicAuction', 'electronicSubmission', 'written', 'inPerson'], default='electronicAuction')  # Specify the method by which bids must be submitted, in person, written, or electronic auction
    submissionMethodDetails = StringType()  # Any detailed or further information on the submission method.
    submissionMethodDetails_en = StringType()
    submissionMethodDetails_ru = StringType()
    enquiryPeriod = ModelType(AuctionPeriodEndRequired, required=True)  # The period during which enquiries may be made and will be answered.
    tenderPeriod = ModelType(AuctionPeriodEndRequired, required=True)  # The period when the auction is open for submissions. The end date is the closing date for auction submissions.
    hasEnquiries = BooleanType()  # A Yes/No field as to whether enquiries were part of auction process.
    eligibilityCriteria = StringType()  # A description of any eligibility criteria for potential suppliers.
    eligibilityCriteria_en = StringType()
    eligibilityCriteria_ru = StringType()
    awardPeriod = ModelType(Period)  # The date or period on which an award is anticipated to be made.
    numberOfBidders = IntType()  # The number of unique tenderers who participated in the auction
    #numberOfBids = IntType()  # The number of bids or submissions to the auction. In the case of an auction, the number of bids may differ from the numberOfBidders.
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.
    procuringEntity = ModelType(ProcuringEntity, required=True)  # The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the auction.
    awards = ListType(ModelType(Award), default=list())
    contracts = ListType(ModelType(Contract), default=list())
    revisions = ListType(ModelType(Revision), default=list())
    auctionPeriod = ModelType(AuctionAuctionPeriod, default={})

    minimalStep = ModelType(Value, required=True)
    status = StringType(choices=['draft', 'active.enquiries', 'active.tendering', 'active.auction', 'active.qualification', 'active.awarded', 'complete', 'cancelled', 'unsuccessful'], default='active.enquiries')
    questions = ListType(ModelType(Question), default=list())
    complaints = ListType(ComplaintModelType(Complaint), default=list())
    auctionUrl = URLType()
    mode = StringType(choices=['test'])
    cancellations = ListType(ModelType(Cancellation), default=list())
    features = ListType(ModelType(Feature), validators=[validate_features_uniq])
    lots = ListType(ModelType(Lot), default=list(), validators=[validate_lots_uniq])
    guarantee = ModelType(Guarantee)
    if SANDBOX_MODE:
        procurementMethodDetails = StringType()

    _attachments = DictType(DictType(BaseType), default=dict())  # couchdb attachments
    dateModified = IsoDateTimeType()
    owner_token = StringType()
    owner = StringType()

    procurementMethodType = StringType(default="belowThreshold")

    create_accreditation = 1
    edit_accreditation = 2
    procuring_entity_kinds = ['general', 'special', 'defense', 'other', '']
    block_complaint_status = ['claim', 'answered', 'pending']

    __name__ = ''

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'chronograph':
            role = 'chronograph'
        elif request.authenticated_role == 'auction':
            role = 'auction_{}'.format(request.method.lower())
        elif request.authenticated_role == 'contracting':
            role = 'contracting'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(i.owner, i.owner_token), 'create_award_complaint')
            for i in self.bids
        ]
        acl.extend([
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_auction_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_complaint'),
        ])
        return acl

    def __repr__(self):
        return '<%s:%r@%r>' % (type(self).__name__, self.id, self.rev)

    def initialize(self):
        if not self.enquiryPeriod.startDate:
            self.enquiryPeriod.startDate = get_now()
        if not self.tenderPeriod.startDate:
            self.tenderPeriod.startDate = self.enquiryPeriod.endDate
        now = get_now()
        self.date = now
        if self.lots:
            for lot in self.lots:
                lot.date = now

    @serializable(serialize_when_none=False)
    def next_check(self):
        '''
            Serializable date field for openprocurement.chronograph.
            Chronograph will check Auction for patching status
            to next by workflow
        '''
        now = get_now()
        checks = []
        if self.status == 'active.enquiries' and self.tenderPeriod.startDate:
            checks.append(self.tenderPeriod.startDate.astimezone(TZ))
        elif self.status == 'active.enquiries' and self.enquiryPeriod.endDate:
            checks.append(self.enquiryPeriod.endDate.astimezone(TZ))
        elif self.status == 'active.tendering' and self.tenderPeriod.endDate:
            checks.append(self.tenderPeriod.endDate.astimezone(TZ))
        elif not self.lots and self.status == 'active.auction' and self.auctionPeriod and self.auctionPeriod.startDate and not self.auctionPeriod.endDate:
            if now < self.auctionPeriod.startDate:
                checks.append(self.auctionPeriod.startDate.astimezone(TZ))
            elif now < calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ):
                checks.append(calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ))
        elif self.lots and self.status == 'active.auction':
            for lot in self.lots:
                if lot.status != 'active' or not lot.auctionPeriod or not lot.auctionPeriod.startDate or lot.auctionPeriod.endDate:
                    continue
                if now < lot.auctionPeriod.startDate:
                    checks.append(lot.auctionPeriod.startDate.astimezone(TZ))
                elif now < calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ):
                    checks.append(calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ))
        checks = next_check_awarding(self, checks)  # Use next_chek part from awarding 1.0
        if self.status.startswith('active'):
            from openprocurement.api.utils import calculate_business_date
            for complaint in self.complaints:
                if complaint.status == 'claim' and complaint.dateSubmitted:
                    checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                elif complaint.status == 'answered' and complaint.dateAnswered:
                    checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
            for award in self.awards:
                for complaint in award.complaints:
                    if complaint.status == 'claim' and complaint.dateSubmitted:
                        checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                    elif complaint.status == 'answered' and complaint.dateAnswered:
                        checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
        return min(checks).isoformat() if checks else None

    def validate_procurementMethodDetails(self, *args, **kw):
        if self.mode and self.mode == 'test' and self.procurementMethodDetails and self.procurementMethodDetails != '':
            raise ValidationError(u"procurementMethodDetails should be used with mode test")

    @serializable
    def numberOfBids(self):
        """A property that is serialized by schematics exports."""
        return len(self.bids)

    @serializable(serialized_name='id')
    def doc_id(self):
        """A property that is serialized by schematics exports."""
        return self._id

    @serializable(serialized_name="value", type=ModelType(Value))
    def auction_value(self):
        return Value(dict(amount=sum([i.value.amount for i in self.lots]),
                          currency=self.value.currency,
                          valueAddedTaxIncluded=self.value.valueAddedTaxIncluded)) if self.lots else self.value

    @serializable(serialized_name="guarantee", serialize_when_none=False, type=ModelType(Guarantee))
    def auction_guarantee(self):
        if self.lots:
            lots_amount = [i.guarantee.amount for i in self.lots if i.guarantee]
            if not lots_amount:
                return self.guarantee
            guarantee = {'amount': sum(lots_amount)}
            lots_currency = [i.guarantee.currency for i in self.lots if i.guarantee]
            guarantee['currency'] = lots_currency[0] if lots_currency else None
            if self.guarantee:
                guarantee['currency'] = self.guarantee.currency
            return Guarantee(guarantee)
        else:
            return self.guarantee

    @serializable(serialized_name="minimalStep", type=ModelType(Value))
    def auction_minimalStep(self):
        return Value(dict(amount=min([i.minimalStep.amount for i in self.lots]),
                          currency=self.minimalStep.currency,
                          valueAddedTaxIncluded=self.minimalStep.valueAddedTaxIncluded)) if self.lots else self.minimalStep

    def import_data(self, raw_data, **kw):
        """
        Converts and imports the raw data into the instance of the model
        according to the fields in the model.
        :param raw_data:
            The data to be imported.
        """
        data = self.convert(raw_data, **kw)
        del_keys = [k for k in data.keys() if data[k] == self.__class__.fields[k].default or data[k] == getattr(self, k)]
        for k in del_keys:
            del data[k]

        self._data.update(data)
        return self

    def validate_features(self, data, features):
        if features and data['lots'] and any([
            round(vnmax([
                i
                for i in features
                if i.featureOf == 'tenderer' or i.featureOf == 'lot' and i.relatedItem == lot['id'] or i.featureOf == 'item' and i.relatedItem in [j.id for j in data['items'] if j.relatedLot == lot['id']]
            ]), 15) > 0.3
            for lot in data['lots']
        ]):
            raise ValidationError(u"Sum of max value of all features for lot should be less then or equal to 30%")
        elif features and not data['lots'] and round(vnmax(features), 15) > 0.3:
            raise ValidationError(u"Sum of max value of all features should be less then or equal to 30%")

    def validate_auctionUrl(self, data, url):
        if url and data['lots']:
            raise ValidationError(u"url should be posted for each lot")

    def validate_minimalStep(self, data, value):
        if value and value.amount and data.get('value'):
            if data.get('value').amount < value.amount:
                raise ValidationError(u"value should be less than value of auction")
            if data.get('value').currency != value.currency:
                raise ValidationError(u"currency should be identical to currency of value of auction")
            if data.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                raise ValidationError(u"valueAddedTaxIncluded should be identical to valueAddedTaxIncluded of value of auction")

    def validate_tenderPeriod(self, data, period):
        if period and period.startDate and data.get('enquiryPeriod') and data.get('enquiryPeriod').endDate and period.startDate < data.get('enquiryPeriod').endDate:
            raise ValidationError(u"period should begin after enquiryPeriod")

    def validate_awardPeriod(self, data, period):
        if period and period.startDate and data.get('auctionPeriod') and data.get('auctionPeriod').endDate and period.startDate < data.get('auctionPeriod').endDate:
            raise ValidationError(u"period should begin after auctionPeriod")
        if period and period.startDate and data.get('tenderPeriod') and data.get('tenderPeriod').endDate and period.startDate < data.get('tenderPeriod').endDate:
            raise ValidationError(u"period should begin after tenderPeriod")

    def validate_lots(self, data, value):
        if len(set([lot.guarantee.currency for lot in value if lot.guarantee])) > 1:
            raise ValidationError(u"lot guarantee currency should be identical to auction guarantee currency")
