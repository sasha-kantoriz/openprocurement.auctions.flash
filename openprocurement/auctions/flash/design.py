# -*- coding: utf-8 -*-
from couchdb.design import ViewDefinition
from openprocurement.api import design


FIELDS = [
    'auctionPeriod',
    'status',
    'auctionID',
    'lots',
    'procurementMethodType',
]
CHANGES_FIELDS = FIELDS + [
    'dateModified',
]


def add_design():
    for i, j in globals().items():
        if "_view" in i:
            setattr(design, i, j)


auctions_all_view = ViewDefinition('auctions', 'all', '''function(doc) {
    if(doc.doc_type == 'Auction') {
        emit(doc.auctionID, null);
    }
}''')


auctions_by_dateModified_view = ViewDefinition('auctions', 'by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Auction') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

auctions_real_by_dateModified_view = ViewDefinition('auctions', 'real_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Auction' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

auctions_test_by_dateModified_view = ViewDefinition('auctions', 'test_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Auction' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

auctions_by_local_seq_view = ViewDefinition('auctions', 'by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Auction') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

auctions_real_by_local_seq_view = ViewDefinition('auctions', 'real_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Auction' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

auctions_test_by_local_seq_view = ViewDefinition('auctions', 'test_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Auction' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

conflicts_view = ViewDefinition('conflicts', 'all', '''function(doc) {
    if (doc._conflicts) {
        emit(doc._rev, [doc._rev].concat(doc._conflicts));
    }
}''')
