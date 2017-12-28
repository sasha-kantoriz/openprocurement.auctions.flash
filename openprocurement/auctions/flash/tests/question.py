# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.tests.base import BaseAuctionWebTest, test_lots
from openprocurement.auctions.flash.tests.blanks.question_blanks import (
    # AuctionQuestionResourceTest
    create_auction_question_invalid,
    create_auction_question,
    patch_auction_question,
    get_auction_question,
    get_auction_questions,
    # AuctionLotQuestionResourceTest
    create_auction_lot_question,
    patch_auction_lot_question
)


class AuctionQuestionResourceTest(BaseAuctionWebTest):
    test_create_auction_question_invalid = snitch(create_auction_question_invalid)
    test_create_auction_question = snitch(create_auction_question)
    test_patch_auction_question = snitch(patch_auction_question)
    test_get_auction_question = snitch(get_auction_question)
    test_get_auction_questions = snitch(get_auction_questions)


class AuctionLotQuestionResourceTest(BaseAuctionWebTest):
    initial_lots = 2 * test_lots
    test_create_auction_lot_question = snitch(create_auction_lot_question)
    test_patch_auction_lot_question = snitch(patch_auction_lot_question)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionQuestionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotQuestionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
