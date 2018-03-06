# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.award import (
    AuctionLotAwardResourceTestMixin,
    Auction2LotAwardResourceTestMixin,
    AuctionAwardDocumentResourceTestMixin,
    AuctionLotAwardComplaintResourceTestMixin,
    Auction2LotAwardComplaintResourceTestMixin,
    AuctionAwardComplaintDocumentResourceTestMixin,
    Auction2LotAwardComplaintDocumentResourceTestMixin,
    Auction2LotAwardDocumentResourceTestMixin
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.flash.tests.base import (
    BaseAuctionWebTest,
    test_bids,
    test_lots,
    test_organization
)

from openprocurement.auctions.core.plugins.awarding.v1.tests.blanks.award_blanks import (
    # AuctionAwardResourceTest
    create_auction_award_invalid,
    create_auction_award,
    patch_auction_award,
    patch_auction_award_unsuccessful,
    get_auction_award,
    patch_auction_award_Administrator_change,
    # AuctionAwardComplaintResourceTest
    create_auction_award_complaint_invalid,
    create_auction_award_complaint,
    patch_auction_award_complaint,
    review_auction_award_complaint,
    get_auction_award_complaint,
    get_auction_award_complaints
)


class AuctionAwardResourceTest(BaseAuctionWebTest):
    #initial_data = auction_data
    initial_status = 'active.qualification'
    initial_bids = test_bids
    test_create_auction_award_invalid = snitch(create_auction_award_invalid)
    test_create_auction_award = snitch(create_auction_award)
    test_patch_auction_award = snitch(patch_auction_award)
    test_patch_auction_award_unsuccessful = snitch(patch_auction_award_unsuccessful)
    test_get_auction_award = snitch(get_auction_award)
    test_patch_auction_award_Administrator_change = snitch(patch_auction_award_Administrator_change)

    def test_create_auction_award_invalid(self):
        request_path = '/auctions/{}/awards'.format(self.auction_id)
        response = self.app.post(request_path, 'data', status=415)
        self.assertEqual(response.status, '415 Unsupported Media Type')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description':
                u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
        ])

class AuctionLotAwardResourceTest(BaseAuctionWebTest, AuctionLotAwardResourceTestMixin):
    initial_status = 'active.qualification'
    initial_lots = test_lots
    initial_bids = test_bids
    initial_organization = test_organization

    def test_create_auction_award(self):
        request_path = '/auctions/{}/awards'.format(self.auction_id)
        response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'], [
            {"location": "body", "name": "lotID", "description": ["This field is required."]}
        ])

class Auction2LotAwardResourceTest(BaseAuctionWebTest, Auction2LotAwardResourceTestMixin):
    initial_status = 'active.qualification'
    initial_lots = 2 * test_lots
    initial_bids = test_bids
    initial_organization = test_organization


class AuctionAwardComplaintResourceTest(BaseAuctionWebTest):
    #initial_data = auction_data
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionAwardComplaintResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id),
            {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']

    test_create_auction_award_complaint_invalid = snitch(create_auction_award_complaint_invalid)
    test_create_auction_award_complaint = snitch(create_auction_award_complaint)
    test_patch_auction_award_complaint = snitch(patch_auction_award_complaint)
    test_review_auction_award_complaint = snitch(review_auction_award_complaint)
    test_get_auction_award_complaint = snitch(get_auction_award_complaint)
    test_get_auction_award_complaints = snitch(get_auction_award_complaints)


class AuctionLotAwardComplaintResourceTest(BaseAuctionWebTest,
                                           AuctionLotAwardComplaintResourceTestMixin):
    initial_status = 'active.qualification'
    initial_lots = test_lots
    initial_bids = test_bids
    initial_organization = test_organization

    def setUp(self):
        super(AuctionLotAwardComplaintResourceTest, self).setUp()
        # Create award
        bid = self.initial_bids[0]
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id'], 'lotID': bid['lotValues'][0]['relatedLot']}})
        award = response.json['data']
        self.award_id = award['id']

    def test_create_auction_award_complaint(self):
        response = self.app.post_json('/auctions/{}/awards/{}/complaints'.format(
            self.auction_id, self.award_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization, 'status': 'claim'}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        complaint = response.json['data']
        self.assertEqual(complaint['author']['name'], test_organization['name'])
        self.assertIn('id', complaint)
        self.assertIn(complaint['id'], response.headers['Location'])

class Auction2LotAwardComplaintResourceTest(BaseAuctionWebTest,
                                            Auction2LotAwardComplaintResourceTestMixin):
    initial_status = 'active.qualification'
    initial_lots = 2 * test_lots
    initial_bids = test_bids
    initial_organization = test_organization

    def setUp(self):
        super(Auction2LotAwardComplaintResourceTest, self).setUp()
        # Create award
        bid = self.initial_bids[0]
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id'], 'lotID': bid['lotValues'][0]['relatedLot']}})
        award = response.json['data']
        self.award_id = award['id']

    test_get_auction_lot_award_complaint = snitch(get_auction_award_complaint)
    test_get_auction_lot_award_complaints = snitch(get_auction_award_complaints)

        response = self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(self.auction_id, self.award_id, complaint['id'], self.auction_token), {"data": {
            "status": "answered",
            "resolutionType": "invalid",
            "resolution": "spam 100% " * 3
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "answered")
        self.assertEqual(response.json['data']["resolutionType"], "invalid")
        self.assertEqual(response.json['data']["resolution"], "spam 100% " * 3)

class AuctionAwardComplaintDocumentResourceTest(BaseAuctionWebTest,
                                                AuctionAwardComplaintDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionAwardComplaintDocumentResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']
        # Create complaint for award
        response = self.app.post_json('/auctions/{}/awards/{}/complaints'.format(
            self.auction_id, self.award_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']

    def test_not_found(self):
        response = self.app.post('/auctions/some_id/awards/some_id/complaints/some_id/documents', status=404, upload_files=[
                                 ('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'auction_id'}
        ])

class Auction2LotAwardComplaintDocumentResourceTest(BaseAuctionWebTest,
                                                    Auction2LotAwardComplaintDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotAwardComplaintDocumentResourceTest, self).setUp()
        # Create award
        bid = self.initial_bids[0]
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id'], 'lotID': bid['lotValues'][0]['relatedLot']}})
        award = response.json['data']
        self.award_id = award['id']
        # Create complaint for award
        response = self.app.post_json('/auctions/{}/awards/{}/complaints'.format(
            self.auction_id, self.award_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']

    def test_create_auction_award_complaint_document(self):
        response = self.app.post('/auctions/{}/awards/{}/complaints/{}/documents'.format(
            self.auction_id, self.award_id, self.complaint_id), upload_files=[('file', 'name.doc', 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (draft) complaint status")

class AuctionAwardDocumentResourceTest(BaseAuctionWebTest,
                                       AuctionAwardDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(AuctionAwardDocumentResourceTest, self).setUp()
        # Create award
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.first_award_id = award['id']

    def test_not_found(self):
        response = self.app.post('/auctions/some_id/awards/some_id/documents', status=404, upload_files=[
                                 ('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'auction_id'}
        ])

class Auction2LotAwardDocumentResourceTest(BaseAuctionWebTest,
                                           Auction2LotAwardDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Auction2LotAwardDocumentResourceTest, self).setUp()
        # Create award
        bid = self.initial_bids[0]
        response = self.app.post_json('/auctions/{}/awards'.format(
            self.auction_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id'], 'lotID': bid['lotValues'][0]['relatedLot']}})
        award = response.json['data']
        self.award_id = award['id']

    def test_create_auction_award_document(self):
        response = self.app.post('/auctions/{}/awards/{}/documents'.format(
            self.auction_id, self.award_id), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('name.doc', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/auctions/{}/awards/{}/documents'.format(self.auction_id, self.award_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/auctions/{}/awards/{}/documents?all=true'.format(self.auction_id, self.award_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/auctions/{}/awards/{}/documents/{}?download=some_id'.format(
            self.auction_id, self.award_id, doc_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
        ])

        response = self.app.get('/auctions/{}/awards/{}/documents/{}?{}'.format(
            self.auction_id, self.award_id, doc_id, key))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 7)
        self.assertEqual(response.body, 'content')

        response = self.app.get('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        response = self.app.post_json('/auctions/{}/cancellations'.format(self.auction_id), {'data': {
            'reason': 'cancellation reason',
            'status': 'active',
            "cancellationOf": "lot",
            "relatedLot": self.initial_lots[0]['id']
        }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.post('/auctions/{}/awards/{}/documents'.format(
            self.auction_id, self.award_id), upload_files=[('file', 'name.doc', 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can add document only in active lot status")

    def test_put_auction_award_document(self):
        response = self.app.post('/auctions/{}/awards/{}/documents'.format(
            self.auction_id, self.award_id), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.put('/auctions/{}/awards/{}/documents/{}'.format(self.auction_id, self.award_id, doc_id),
                                status=404,
                                upload_files=[('invalid_name', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'body', u'name': u'file'}
        ])

        response = self.app.put('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id), upload_files=[('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/auctions/{}/awards/{}/documents/{}?{}'.format(
            self.auction_id, self.award_id, doc_id, key))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content2')

        response = self.app.get('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        response = self.app.put('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id), 'content3', content_type='application/msword')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/auctions/{}/awards/{}/documents/{}?{}'.format(
            self.auction_id, self.award_id, doc_id, key))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content3')

        response = self.app.post_json('/auctions/{}/cancellations'.format(self.auction_id), {'data': {
            'reason': 'cancellation reason',
            'status': 'active',
            "cancellationOf": "lot",
            "relatedLot": self.initial_lots[0]['id']
        }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.put('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id), upload_files=[('file', 'name.doc', 'content3')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can update document only in active lot status")

    def test_patch_auction_award_document(self):
        response = self.app.post('/auctions/{}/awards/{}/documents'.format(
            self.auction_id, self.award_id), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}'.format(self.auction_id, self.award_id, doc_id), {"data": {"description": "document description"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])

        response = self.app.get('/auctions/{}/awards/{}/documents/{}'.format(
            self.auction_id, self.award_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('document description', response.json["data"]["description"])

        response = self.app.post_json('/auctions/{}/cancellations'.format(self.auction_id), {'data': {
            'reason': 'cancellation reason',
            'status': 'active',
            "cancellationOf": "lot",
            "relatedLot": self.initial_lots[0]['id']
        }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}'.format(self.auction_id, self.award_id, doc_id), {"data": {"description": "document description"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can update document only in active lot status")


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionAwardResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotAwardResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotAwardResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAwardComplaintResourceTest))
    tests.addTest(unittest.makeSuite(AuctionLotAwardComplaintResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotAwardComplaintResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAwardComplaintDocumentResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotAwardComplaintDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AuctionAwardDocumentResourceTest))
    tests.addTest(unittest.makeSuite(Auction2LotAwardDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
