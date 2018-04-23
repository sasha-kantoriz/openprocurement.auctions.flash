from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    IAwardingNextCheck,
    IContentConfigurator
)
from openprocurement.auctions.core.plugins.awarding.v1.adapters import (
    AwardingNextCheckV1
)

from openprocurement.auctions.flash.models import Auction, IFlashAuction
from openprocurement.auctions.flash.adapters import AuctionFlashConfigurator
from openprocurement.auctions.flash.constants import (
    VIEW_LOCATIONS,
    DEFAULT_PROCUREMENT_METHOD_TYPE
)


def includeme(config, plugin_config=None):
    procurement_method_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(Auction,
                                                 procurementMethodType)

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
