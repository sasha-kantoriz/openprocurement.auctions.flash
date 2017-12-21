# -*- coding: utf-8 -*-
from openprocurement.auctions.core.adapters import AuctionConfigurator
from openprocurement.auctions.flash.models import Auction


class AuctionFlashConfigurator(AuctionConfigurator):
    name = 'Auction Flash Configurator'
    model = Auction