# -*- coding: utf-8 -*-
from openprocurement.auctions.flash.tests.base import test_auction_data
from openprocurement.auctions.flash.models import Auction
from openprocurement.auctions.flash.migration import migrate_data, set_db_schema_version

# MigrateTest


def migrate_from0to1(self):
    set_db_schema_version(self.db, 0)
    u = Auction(test_auction_data)
    u.auctionID = "UA-X"
    u.store(self.db)
    data = self.db.get(u.id)
    data["documents"] = [
        {
            "id": "ebcb5dd7f7384b0fbfbed2dc4252fa6e",
            "title": "name.txt",
            "url": "/tenders/{}/documents/ebcb5dd7f7384b0fbfbed2dc4252fa6e?download=10367238a2964ee18513f209d9b6d1d3".format(u.id),
            "datePublished": "2016-06-01T00:00:00+03:00",
            "dateModified": "2016-06-01T00:00:00+03:00",
            "format": "text/plain",
        }
    ]
    _id, _rev = self.db.save(data)
    self.app.app.registry.docservice_url = 'http://localhost'
    migrate_data(self.app.app.registry, 1)
    migrated_item = self.db.get(u.id)
    self.assertIn('http://localhost/get/10367238a2964ee18513f209d9b6d1d3?', migrated_item['documents'][0]['url'])
    self.assertIn('Prefix={}%2Febcb5dd7f7384b0fbfbed2dc4252fa6e'.format(u.id), migrated_item['documents'][0]['url'])
    self.assertIn('KeyID=', migrated_item['documents'][0]['url'])
    self.assertIn('Signature=', migrated_item['documents'][0]['url'])
