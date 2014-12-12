from django.conf.urls import patterns, include, url
from tastypie.api import Api
from webservice.api import AccountResource, AddressResource, ClientResource


v0_api = Api(api_name='v0')
v0_api.register(AccountResource())
v0_api.register(AddressResource())
v0_api.register(ClientResource())

urlpatterns = patterns('',
    url(r'^api/', include(v0_api.urls)),
    url(r'^api/{}/doc/'.format(v0_api.api_name), include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)
