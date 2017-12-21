from pyramid.interfaces import IRequest
from openprocurement.auctions.flash.models import Auction, IAuctionFlash
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.auctions.flash.adapters import AuctionFlashConfigurator


def includeme(config):
    config.add_auction_procurementMethodType(Auction)
    config.scan("openprocurement.auctions.flash.views")
    config.registry.registerAdapter(AuctionFlashConfigurator, (IAuctionFlash, IRequest),
                                    IContentConfigurator)