# -*- coding: utf-8 -*-

import unittest

from openprocurement.auctions.flash.tests import auction, award, bidder, document, migration, spore, auction, question, complaint


def suite():
    suite = unittest.TestSuite()
    suite.addTest(auction.suite())
    suite.addTest(award.suite())
    suite.addTest(bidder.suite())
    suite.addTest(complaint.suite())
    suite.addTest(document.suite())
    suite.addTest(migration.suite())
    suite.addTest(question.suite())
    suite.addTest(spore.suite())
    suite.addTest(auction.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
