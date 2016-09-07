from openprocurement.auctions.flash.models import Auction


def includeme(config):
    config.add_auction_procurementMethodType(Auction)
    config.scan("openprocurement.auctions.flash.views")
