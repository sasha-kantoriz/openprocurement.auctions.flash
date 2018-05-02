# -*- coding: utf-8 -*-
import os
import webtest
from datetime import datetime, timedelta

from openprocurement.auctions.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
    BaseAuctionWebTest as CoreBaseAuctionWebTest,
    base_test_bids as test_bids,  # noqa forwarded import
    test_organization,
)
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE,
    VERSION,
)

from openprocurement.auctions.flash.constants import DEFAULT_PROCUREMENT_METHOD_TYPE


now = datetime.now()
test_procuringEntity = test_organization.copy()
test_auction_data = {
    "title": u"футляри до державних нагород",
    "procuringEntity": test_procuringEntity,
    "value": {
        "amount": 100,
        "currency": u"UAH"
    },
    "minimalStep": {
        "amount": 35,
        "currency": u"UAH"
    },
    "items": [
        {
            "description": u"Земля для військовослужбовців",
            "classification": {
                "scheme": u"CAV",
                "id": u"70122000-2",
                "description": u"Земля"
            },
            "additionalClassifications": [
                {
                    "scheme": u"ДКПП",
                    "id": u"17.21.1",
                    "description": u"папір і картон гофровані, паперова й картонна тара"
                }
            ],
            "unit": {
                "name": u"item",
                "code": u"44617100-9"
            },
            "quantity": 5,
            "deliveryDate": {
                "startDate": (now + timedelta(days=2)).isoformat(),
                "endDate": (now + timedelta(days=5)).isoformat()
            },
            "deliveryAddress": {
                "countryName": u"Україна",
                "postalCode": "79000",
                "region": u"м. Київ",
                "locality": u"м. Київ",
                "streetAddress": u"вул. Банкова 1"
            }
        }
    ],
    "enquiryPeriod": {
        "endDate": (now + timedelta(days=7)).isoformat()
    },
    "tenderPeriod": {
        "endDate": (now + timedelta(days=14)).isoformat()
    },
    "procurementMethodType": DEFAULT_PROCUREMENT_METHOD_TYPE,
}
if SANDBOX_MODE:
    test_auction_data['procurementMethodDetails'] = 'quick, accelerator=1440'
test_features_auction_data = test_auction_data.copy()
test_features_item = test_features_auction_data['items'][0].copy()
test_features_item['id'] = "1"
test_features_auction_data['items'] = [test_features_item]
test_features_auction_data["features"] = [
    {
        "code": "OCDS-123454-AIR-INTAKE",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"Потужність всмоктування",
        "title_en": "Air Intake",
        "description": u"Ефективна потужність всмоктування пилососа, в ватах (аероватах)",
        "enum": [
            {
                "value": 0.1,
                "title": u"До 1000 Вт"
            },
            {
                "value": 0.15,
                "title": u"Більше 1000 Вт"
            }
        ]
    },
    {
        "code": "OCDS-123454-YEARS",
        "featureOf": "tenderer",
        "title": u"Років на ринку",
        "title_en": "Years trading",
        "description": u"Кількість років, які організація учасник працює на ринку",
        "enum": [
            {
                "value": 0.05,
                "title": u"До 3 років"
            },
            {
                "value": 0.1,
                "title": u"Більше 3 років, менше 5 років"
            },
            {
                "value": 0.15,
                "title": u"Більше 5 років"
            }
        ]
    }
]
test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]
test_features = [
    {
        "code": "code_item",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"item feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    },
    {
        "code": "code_tenderer",
        "featureOf": "tenderer",
        "title": u"tenderer feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    }
]


class PrefixedRequestClass(webtest.app.TestRequest):

    @classmethod
    def blank(cls, path, *args, **kwargs):
        path = '/api/%s%s' % (VERSION, path)
        return webtest.app.TestRequest.blank(path, *args, **kwargs)


class BaseWebTest(CoreBaseWebTest):

    """Base Web Test to test openprocurement.auctions.flash.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)


class BaseAuctionWebTest(CoreBaseAuctionWebTest):
    initial_data = test_auction_data
    relative_to = os.path.dirname(__file__)