from pyramid.interfaces import IRequest

from openprocurement.api.interfaces import (
    IContentConfigurator,
    IAwardingNextCheck
)
from openprocurement.auctions.core.plugins.awarding.v1.adapters import (
    AwardingNextCheckV1
)
from openprocurement.auctions.flash.models import Auction, IFlashAuction
from openprocurement.auctions.flash.adapters import AuctionFlashConfigurator
from openprocurement.auctions.flash.constants import VIEW_LOCATIONS


def includeme(config):
    config.add_auction_procurementMethodType(Auction)

    # add views
    for view_location in VIEW_LOCATIONS:
        config.scan(view_location)

    # register adapters
    config.registry.registerAdapter(
        AuctionFlashConfigurator,
        (IFlashAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AwardingNextCheckV1,
        (IFlashAuction, ),
        IAwardingNextCheck
    )
