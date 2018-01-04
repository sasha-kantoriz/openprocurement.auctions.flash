# -*- coding: utf-8 -*-

# AuctionLotResourceTest


def patch_auction_currency(self):
    # create lot
    response = self.app.post_json('/auctions/{}/lots'.format(self.auction_id), {'data': self.test_lots[0]})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    lot = response.json['data']
    self.assertEqual(lot['value']['currency'], "UAH")

    # update auction currency without mimimalStep currency change
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {"data": {"value": {"currency": "GBP"}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'currency should be identical to currency of value of auction'],
         u'location': u'body', u'name': u'minimalStep'}
    ])

    # update auction currency
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {"data": {
        "value": {"currency": "GBP"},
        "minimalStep": {"currency": "GBP"}
    }})
    self.assertEqual(response.status, '200 OK')
    # log currency is updated too
    response = self.app.get('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    lot = response.json['data']
    self.assertEqual(lot['value']['currency'], "GBP")

    # try to update lot currency
    response = self.app.patch_json('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']), {"data": {"value": {"currency": "USD"}}})
    self.assertEqual(response.status, '200 OK')
    # but the value stays unchanged
    response = self.app.get('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    lot = response.json['data']
    self.assertEqual(lot['value']['currency'], "GBP")

    # try to update minimalStep currency
    response = self.app.patch_json('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']), {"data": {"minimalStep": {"currency": "USD"}}})
    self.assertEqual(response.status, '200 OK')
    # but the value stays unchanged
    response = self.app.get('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    lot = response.json['data']
    self.assertEqual(lot['minimalStep']['currency'], "GBP")

    # try to update lot minimalStep currency and lot value currency in single request
    response = self.app.patch_json('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']), {"data": {"value": {"currency": "USD"},
                                                                                                      "minimalStep": {"currency": "USD"}}})
    self.assertEqual(response.status, '200 OK')
    # but the value stays unchanged
    response = self.app.get('/auctions/{}/lots/{}'.format(self.auction_id, lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    lot = response.json['data']
    self.assertEqual(lot['value']['currency'], "GBP")
    self.assertEqual(lot['minimalStep']['currency'], "GBP")
