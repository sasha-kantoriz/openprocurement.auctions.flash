# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import AuctionConfigurator
from openprocurement.auctions.flash.models import Auction
from openprocurement.auctions.core.plugins.awarding.v1.utils import add_next_award
from openprocurement.auctions.core.plugins.awarding.v1.models import Award


class AuctionFlashConfigurator(AuctionConfigurator):
    name = 'Auction Flash Configurator'
    model = Auction
    award_model = Award

    def add_award(self):
        return add_next_award(self.request)
