# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.flash.migration import migrate_data
from openprocurement.auctions.flash.tests.base import BaseWebTest
from openprocurement.auctions.flash.tests.blanks.migration_blanks import migrate, migrate_from0to1


class MigrateTest(BaseWebTest):
    def setUp(self):
        super(MigrateTest, self).setUp()
        migrate_data(self.app.app.registry)

    test_migrate = snitch(migrate)
    test_migrate_from0to1 = snitch(migrate_from0to1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MigrateTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
