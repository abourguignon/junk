import json
import logging

from tastypie import http
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
import zmq
from zmq.log.handlers import PUBHandler

from webservice.models import Account, Address, Client



# ZMQ logging: create a PUB handler and append it to the 'api' logger
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind('tcp://*:12345')
handler = PUBHandler(sock)
handler.formatters[logging.INFO] = logging.Formatter("%(asctime)s %(message)s\n")  # the default formatter doesn't include time

logger = logging.getLogger('api')
logger.addHandler(handler)


class PrettyJSONSerializer(Serializer):
    json_indent = 4

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data, sort_keys=True, ensure_ascii=False, indent=self.json_indent)


class CustomModelResource(ModelResource):
    def dispatch(self, request_type, request, **kwargs):
        """
        Override for systematic logging.
        """
        log_user = request.META['USER']
        log_request_type = request_type
        log_resource_name = kwargs['resource_name']
        log_api_name = kwargs['api_name']

        try:
            response = super(CustomModelResource, self).dispatch(request_type, request, **kwargs)
            log_response_code = response.status_code
            log_response_body = json.loads(response.content)

        except Exception, e:
            log_response_code = http.HttpBadRequest.status_code
            log_response_body = e.__class__.__name__ + e.message
            raise
        finally:
            logger.info('%s asked for %s on %s through api %s: \n%s\n%s' % (
                log_user,
                log_request_type,
                log_resource_name,
                log_api_name,
                log_response_code,
                log_response_body,
            ))

        return response

    class Meta:
        serializer = PrettyJSONSerializer()
        authentication = BasicAuthentication()


class AccountResource(CustomModelResource):
    class Meta(CustomModelResource.Meta):
        queryset = Account.objects.all()
        resource_name = 'account'


class AddressResource(CustomModelResource):
    class Meta(CustomModelResource.Meta):
        queryset = Address.objects.all()
        resource_name = 'address'


class ClientResource(CustomModelResource):
    class Meta(CustomModelResource.Meta):
        queryset = Client.objects.all()
        resource_name = 'client'
