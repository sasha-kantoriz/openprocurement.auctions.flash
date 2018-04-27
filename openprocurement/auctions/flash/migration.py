# -*- coding: utf-8 -*-
import logging

from pyramid.config import Configurator

from openprocurement.auctions.core.traversal import Root
from openprocurement.auctions.core.utils import get_plugins, read_yaml

from openprocurement.auctions.flash.models import Auction

LOGGER = logging.getLogger(__name__)
SCHEMA_VERSION = 1
SCHEMA_DOC = 'openprocurement_auctions_flash_schema'


def get_db_schema_version(db):
    schema_doc = db.get(SCHEMA_DOC, {"_id": SCHEMA_DOC})
    return schema_doc.get("version", SCHEMA_VERSION - 1)


def set_db_schema_version(db, version):
    schema_doc = db.get(SCHEMA_DOC, {"_id": SCHEMA_DOC})
    schema_doc["version"] = version
    db.save(schema_doc)


def migrate_data(registry, destination=None):
    if isinstance(registry, Configurator):
        registry = registry.registry
    plugins_config = registry.app_meta(['plugins'])
    existing_plugins = get_plugins(plugins_config)
    if registry.app_meta(['plugins']) and 'auctions.core' not in existing_plugins:
        return
    cur_version = get_db_schema_version(registry.db)
    if cur_version == SCHEMA_VERSION:
        return cur_version
    for step in xrange(cur_version, destination or SCHEMA_VERSION):
        LOGGER.info("Migrate flash auctions schema from {} to {}".format(step, step + 1), extra={'MESSAGE_ID': 'migrate_data'})
        migration_func = globals().get('from{}to{}'.format(step, step + 1))
        if migration_func:
            migration_func(registry)
        set_db_schema_version(registry.db, step + 1)


def from0to1(registry):
    class Request(object):
        def __init__(self, registry):
            self.registry = registry
    results = registry.db.iterview('auctions/all', 2 ** 10, include_docs=True)
    docs = []
    request = Request(registry)
    root = Root(request)
    pmtConfigurator = registry.pmtConfigurator
    procurement_method_types = [
        pmt for pmt in pmtConfigurator
        if pmtConfigurator[pmt] == "belowThreshold"
    ]
    for i in results:
        doc = i.doc
        if doc['procurementMethodType'] not in procurement_method_types:
            continue
        auction = Auction(doc)
        auction.__parent__ = root
        docs.append(auction.to_primitive())
        if len(docs) >= 2 ** 7:
            result = registry.db.update(docs)
            docs = []
    if docs:
        registry.db.update(docs)
