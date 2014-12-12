from django.contrib import admin
from webservice.models import Account, Address, Client


class AccountAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'client')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'address')


admin.site.register(Address)

admin.site.register(Account, AccountAdmin)
admin.site.register(Client, ClientAdmin)
