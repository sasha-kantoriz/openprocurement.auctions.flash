from pyramid.events import ContextFound
from openprocurement.auctions.flash.design import add_design
from openprocurement.auctions.flash.utils import auction_from_data, extract_auction, set_logging_context


def includeme(config):
    add_design()
    config.add_subscriber(set_logging_context, ContextFound)
    config.add_request_method(extract_auction, 'auction', reify=True)
    config.add_request_method(auction_from_data)
    config.scan("openprocurement.auctions.flash.views")
