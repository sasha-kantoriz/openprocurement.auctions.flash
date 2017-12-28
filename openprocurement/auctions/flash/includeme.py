from pyramid.interfaces import IRequest
from openprocurement.auctions.flash.models import Auction
from openprocurement.auctions.core.models import IAuction
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.auctions.flash.adapters import AuctionFlashConfigurator
from openprocurement.auctions.flash.constants import VIEW_LOCATIONS


def includeme(config):
    config.add_auction_procurementMethodType(Auction)

    for view_location in VIEW_LOCATIONS:
        config.scan(view_location)

    config.registry.registerAdapter(
        AuctionFlashConfigurator,
        (IAuction, IRequest),
        IContentConfigurator
    )

