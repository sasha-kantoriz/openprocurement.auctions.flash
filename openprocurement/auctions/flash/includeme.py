import os
from pyramid.interfaces import IRequest
from openprocurement.auctions.core.includeme import (
    IAwardingNextCheck,
    IContentConfigurator
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.plugins.awarding.v1.adapters import (
    AwardingNextCheckV1
)
from openprocurement.auctions.core.includeme import get_evenly_plugins
from openprocurement.auctions.flash.models import Auction, IFlashAuction
from openprocurement.auctions.flash.adapters import (
    AuctionFlashConfigurator,
    AuctionFlashManagerAdapter
)
from openprocurement.auctions.flash.constants import (
    VIEW_LOCATIONS,
    DEFAULT_PROCUREMENT_METHOD_TYPE
)


def includeme(config, plugin_map):
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
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
    config.registry.registerAdapter(
        AuctionFlashManagerAdapter,
        (IFlashAuction, ),
        IAuctionManager
    )
    # migrate data
    if plugin_map['migration'] and not os.environ.get('MIGRATION_SKIP'):
        get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.auctions.flash.plugins')
