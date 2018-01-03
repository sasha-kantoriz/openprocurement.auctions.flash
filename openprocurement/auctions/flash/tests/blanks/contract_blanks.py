# -*- coding: utf-8 -*-
from datetime import timedelta

from openprocurement.api.models import get_now

# AuctionContractResourceTest


def patch_auction_contract(self):
    response = self.app.get('/auctions/{}/contracts'.format( self.auction_id))
    contract = response.json['data'][0]

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn("Can't sign contract before stand-still period end (", response.json['errors'][0]["description"])

    self.set_status('complete', {'status': 'active.awarded'})

    response = self.app.post_json('/auctions/{}/awards/{}/complaints'.format(self.auction_id, self.award_id), {'data': {
        'title': 'complaint title',
        'description': 'complaint description',
        'author': self.initial_organization,
        'status': 'claim'
    }})
    self.assertEqual(response.status, '201 Created')
    complaint = response.json['data']
    owner_token = response.json['access']['token']

    auction = self.db.get(self.auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"contractID": "myselfID", "items": [{"description": "New Description"}], "suppliers": [{"name": "New Name"}]}})

    response = self.app.get('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']))
    self.assertEqual(response.json['data']['contractID'], contract['contractID'])
    self.assertEqual(response.json['data']['items'], contract['items'])
    self.assertEqual(response.json['data']['suppliers'], contract['suppliers'])

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"value": {"currency": "USD"}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can\'t update currency for contract value")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"value": {"valueAddedTaxIncluded": False}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can\'t update valueAddedTaxIncluded for contract value")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"value": {"amount": 99}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Value amount should be greater or equal to awarded amount (100.0)")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"value": {"amount": 238}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['value']['amount'], 238)

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"dateSigned": i['complaintPeriod']['endDate']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'], [{u'description': [u'Contract signature date should be after award complaint period end date ({})'.format(i['complaintPeriod']['endDate'])], u'location': u'body', u'name': u'dateSigned'}])

    one_hour_in_furure = (get_now() + timedelta(hours=1)).isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"dateSigned": one_hour_in_furure}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'], [{u'description': [u"Contract signature date can't be in the future"], u'location': u'body', u'name': u'dateSigned'}])

    custom_signature_date = get_now().isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"dateSigned": custom_signature_date}})
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't sign contract before reviewing all complaints")

    response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(self.auction_id, self.award_id, complaint['id'], self.auction_token), {"data": {
        "status": "answered",
        "resolutionType": "resolved",
        "resolution": "resolution text " * 2
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "answered")
    self.assertEqual(response.json['data']["resolutionType"], "resolved")
    self.assertEqual(response.json['data']["resolution"], "resolution text " * 2)

    response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(self.auction_id, self.award_id, complaint['id'], owner_token), {"data": {
        "satisfied": True,
        "status": "resolved"
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "resolved")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"value": {"amount": 232}}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update contract in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"contractID": "myselfID"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update contract in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"items": [{"description": "New Description"}]}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update contract in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"suppliers": [{"name": "New Name"}]}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update contract in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']), {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update contract in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/some_id'.format(self.auction_id), {"data": {"status": "active"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'contract_id'}
    ])

    response = self.app.patch_json('/auctions/some_id/contracts/some_id', {"data": {"status": "active"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'auction_id'}
    ])

    response = self.app.get('/auctions/{}/contracts/{}'.format(self.auction_id, contract['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")
    self.assertEqual(response.json['data']["value"]['amount'], 238)
    self.assertEqual(response.json['data']['contractID'], contract['contractID'])
    self.assertEqual(response.json['data']['items'], contract['items'])
    self.assertEqual(response.json['data']['suppliers'], contract['suppliers'])
    self.assertEqual(response.json['data']['dateSigned'], custom_signature_date)
