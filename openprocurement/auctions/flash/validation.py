# -*- coding: utf-8 -*-
from openprocurement.api.models import get_now
from openprocurement.api.utils import update_logging_context
from openprocurement.api.validation import validate_json_data, validate_data
from openprocurement.auctions.flash.models import Auction, Bid, Award, Document, Question, Complaint, Contract, Cancellation, Lot


def validate_auction_data(request):
    update_logging_context(request, {'auction_id': '__new__'})

    data = validate_json_data(request)
    if data is None:
        return

    model = request.auction_from_data(data, create=False)
    return validate_data(request, model, data=data)


def validate_patch_auction_data(request):
    return validate_data(request, Auction, True)


def validate_auction_auction_data(request):
    data = validate_patch_auction_data(request)
    auction = request.validated['auction']
    if auction.status != 'active.auction':
        request.errors.add('body', 'data', 'Can\'t {} in current ({}) auction status'.format('report auction results' if request.method == 'POST' else 'update auction urls', auction.status))
        request.errors.status = 403
        return
    lot_id = request.matchdict.get('auction_lot_id')
    if auction.lots and any([i.status != 'active' for i in auction.lots if i.id == lot_id]):
        request.errors.add('body', 'data', 'Can {} only in active lot status'.format('report auction results' if request.method == 'POST' else 'update auction urls'))
        request.errors.status = 403
        return
    if data is not None:
        bids = data.get('bids', [])
        auction_bids_ids = [i.id for i in auction.bids]
        if len(bids) != len(auction.bids):
            request.errors.add('body', 'bids', "Number of auction results did not match the number of auction bids")
            request.errors.status = 422
            return
        if set([i['id'] for i in bids]) != set(auction_bids_ids):
            request.errors.add('body', 'bids', "Auction bids should be identical to the auction bids")
            request.errors.status = 422
            return
        data['bids'] = [x for (y, x) in sorted(zip([auction_bids_ids.index(i['id']) for i in bids], bids))]
        if data.get('lots'):
            auction_lots_ids = [i.id for i in auction.lots]
            if len(data.get('lots', [])) != len(auction.lots):
                request.errors.add('body', 'lots', "Number of lots did not match the number of auction lots")
                request.errors.status = 422
                return
            if set([i['id'] for i in data.get('lots', [])]) != set([i.id for i in auction.lots]):
                request.errors.add('body', 'lots', "Auction lots should be identical to the auction lots")
                request.errors.status = 422
                return
            data['lots'] = [
                x if x['id'] == lot_id else {}
                for (y, x) in sorted(zip([auction_lots_ids.index(i['id']) for i in data.get('lots', [])], data.get('lots', [])))
            ]
        auction_bids_lots_ids = dict([(i.id, [j['relatedLot'] for j in i.lotValues]) for i in auction.bids])
        if auction.lots and any([len(bid['lotValues']) != len(auction_bids_lots_ids.get(bid['id'], [])) for bid in bids]):
            request.errors.add('body', 'bids', [{u'lotValues': [u'Number of lots of auction results did not match the number of auction lots']}])
            request.errors.status = 422
            return
        if auction.lots and any([set([j['relatedLot'] for j in bid['lotValues']]) != set(auction_bids_lots_ids[bid['id']]) for bid in bids]):
            request.errors.add('body', 'bids', [{u'lotValues': [{u'relatedLot': ['relatedLot should be one of lots of bid']}]}])
            request.errors.status = 422
            return
        for bid in data['bids']:
            if 'lotValues' in bid:
                bid['lotValues'] = [
                    x if x['relatedLot'] == lot_id else {}
                    for (y, x) in sorted(zip([auction_bids_lots_ids[bid['id']].index(i['relatedLot']) for i in bid['lotValues']], bid['lotValues']))
                ]
    else:
        data = {}
    if request.method == 'POST':
        now = get_now().isoformat()
        if auction.lots:
            data['lots'] = [{'auctionPeriod': {'endDate': now}} if i.id == lot_id else {} for i in auction.lots]
        else:
            data['auctionPeriod'] = {'endDate': now}
    request.validated['data'] = data


def validate_bid_data(request):
    update_logging_context(request, {'bid_id': '__new__'})
    return validate_data(request, Bid)


def validate_patch_bid_data(request):
    return validate_data(request, Bid, True)


def validate_award_data(request):
    update_logging_context(request, {'award_id': '__new__'})
    return validate_data(request, Award)


def validate_patch_award_data(request):
    return validate_data(request, Award, True)


def validate_patch_document_data(request):
    return validate_data(request, Document, True)


def validate_question_data(request):
    update_logging_context(request, {'question_id': '__new__'})
    return validate_data(request, Question)


def validate_patch_question_data(request):
    return validate_data(request, Question, True)


def validate_complaint_data(request):
    update_logging_context(request, {'complaint_id': '__new__'})
    return validate_data(request, Complaint)


def validate_patch_complaint_data(request):
    return validate_data(request, Complaint, True)


def validate_cancellation_data(request):
    update_logging_context(request, {'cancellation_id': '__new__'})
    return validate_data(request, Cancellation)


def validate_patch_cancellation_data(request):
    return validate_data(request, Cancellation, True)


def validate_contract_data(request):
    update_logging_context(request, {'contract_id': '__new__'})
    return validate_data(request, Contract)


def validate_patch_contract_data(request):
    return validate_data(request, Contract, True)


def validate_lot_data(request):
    update_logging_context(request, {'lot_id': '__new__'})
    return validate_data(request, Lot)


def validate_patch_lot_data(request):
    return validate_data(request, Lot, True)


def validate_file_upload(request):
    update_logging_context(request, {'document_id': '__new__'})
    if 'file' not in request.POST or not hasattr(request.POST['file'], 'filename'):
        request.errors.add('body', 'file', 'Not Found')
        request.errors.status = 404
    else:
        request.validated['file'] = request.POST['file']


def validate_file_update(request):
    if request.content_type == 'multipart/form-data':
        validate_file_upload(request)
