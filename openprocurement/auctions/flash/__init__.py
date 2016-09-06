from openprocurement.auctions.flash.utils import auction_from_data


def includeme(config):
    config.add_request_method(auction_from_data)
    config.scan("openprocurement.auctions.flash.views")