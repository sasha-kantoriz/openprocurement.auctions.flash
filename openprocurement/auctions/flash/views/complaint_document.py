# -*- coding: utf-8 -*-
from logging import getLogger
from openprocurement.api.utils import (
    json_view,
    context_unpack,
    APIResource
)
from openprocurement.auctions.flash.utils import (
    get_file,
    save_auction,
    upload_file,
    apply_patch,
    update_file_content_type,
    opresource,
)
from openprocurement.auctions.flash.validation import (
    validate_file_update,
    validate_file_upload,
    validate_patch_document_data,
)


LOGGER = getLogger(__name__)


STATUS4ROLE = {
    'complaint_owner': ['draft', 'answered'],
    'reviewers': ['pending'],
    'tender_owner': ['claim'],
}


@opresource(name='Auction Complaint Documents',
            collection_path='/auctions/{auction_id}/complaints/{complaint_id}/documents',
            path='/auctions/{auction_id}/complaints/{complaint_id}/documents/{document_id}',
            description="Auction complaint documents")
class AuctionComplaintDocumentResource(APIResource):

    # def __init__(self, request, context):
    #     self.request = request
    #     self.db = request.registry.db

    @json_view(permission='view_auction')
    def collection_get(self):
        """Auction Complaint Documents List"""
        complaint = self.request.validated['complaint']
        if self.request.params.get('all', ''):
            collection_data = [i.serialize("view") for i in complaint['documents']]
        else:
            collection_data = sorted(dict([
                (i.id, i.serialize("view"))
                for i in complaint['documents']
            ]).values(), key=lambda i: i['dateModified'])
        return {'data': collection_data}

    @json_view(validators=(validate_file_upload,), permission='edit_complaint')
    def collection_post(self):
        """Auction Complaint Document Upload
        """
        if self.request.validated['auction_status'] not in ['active.enquiries', 'active.tendering', 'active.auction', 'active.qualification', 'active.awarded']:
            self.request.errors.add('body', 'data', 'Can\'t add document in current ({}) auction status'.format(self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        if self.context.status not in STATUS4ROLE.get(self.request.authenticated_role, []):
            self.request.errors.add('body', 'data', 'Can\'t add document in current ({}) complaint status'.format(self.context.status))
            self.request.errors.status = 403
            return
        document = upload_file(self.request)
        self.request.validated['complaint'].documents.append(document)
        if save_auction(self.request):
            LOGGER.info('Created auction complaint document {}'.format(document.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_complaint_document_create'}, {'document_id': document.id}))
            self.request.response.status = 201
            document_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=document_route, document_id=document.id, _query={})
            return {'data': document.serialize("view")}

    @json_view(permission='view_auction')
    def get(self):
        """Auction Complaint Document Read"""
        if self.request.params.get('download'):
            return get_file(self.request)
        document = self.request.validated['document']
        document_data = document.serialize("view")
        document_data['previousVersions'] = [
            i.serialize("view")
            for i in self.request.validated['documents']
            if i.url != document.url
        ]
        return {'data': document_data}

    @json_view(validators=(validate_file_update,), permission='edit_complaint')
    def put(self):
        """Auction Complaint Document Update"""
        if self.request.validated['auction_status'] not in ['active.enquiries', 'active.tendering', 'active.auction', 'active.qualification', 'active.awarded']:
            self.request.errors.add('body', 'data', 'Can\'t update document in current ({}) auction status'.format(self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        document = upload_file(self.request)
        self.request.validated['complaint'].documents.append(document)
        if save_auction(self.request):
            LOGGER.info('Updated auction complaint document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_complaint_document_put'}))
            return {'data': document.serialize("view")}

    @json_view(content_type="application/json", validators=(validate_patch_document_data,), permission='edit_complaint')
    def patch(self):
        """Auction Complaint Document Update"""
        if self.request.authenticated_role != self.context.author:
            self.request.errors.add('url', 'role', 'Can update document only author {} {}'.format(self.request.authenticated_role, self.context.author))
            self.request.errors.status = 403
            return
        if self.request.validated['auction_status'] not in ['active.enquiries', 'active.tendering', 'active.auction', 'active.qualification', 'active.awarded']:
            self.request.errors.add('body', 'data', 'Can\'t update document in current ({}) auction status'.format(self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        if self.request.validated['complaint'].status not in STATUS4ROLE.get(self.request.authenticated_role, []):
            self.request.errors.add('body', 'data', 'Can\'t update document in current ({}) complaint status'.format(self.request.validated['complaint'].status))
            self.request.errors.status = 403
            return
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            LOGGER.info('Updated auction complaint document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_complaint_document_patch'}))
            return {'data': self.request.context.serialize("view")}
