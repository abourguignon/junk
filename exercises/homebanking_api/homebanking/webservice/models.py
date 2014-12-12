import re

from django.db import models
from django.core.exceptions import ValidationError


def validate_iban(value):
    pattern = r'[A-Z]{2}[0-9]{2}[a-zA-Z-0-9]{1,30}'
    if not re.match(r'[A-Z]{2}[0-9]{2}[a-zA-Z-0-9]{1,30}', value):
        raise ValidationError(u'%s is not in the IBAN format (%s)' % (value, pattern))


class Address(models.Model):
    street = models.TextField(help_text='Number and street')
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s, %s - %s %s' % (self.street, self.city, self.province, self.zip_code)

    class Meta:
        verbose_name_plural = 'addresses'


class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, default=None, null=True, blank=True)
    date_of_birth = models.DateField()
    address = models.ForeignKey(Address)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.date_of_birth)


class Account(models.Model):
    DEPOSIT = 'DEPOSIT'
    SAVINGS = 'SAVINGS'
    OTHER = 'OTHER'
    ACCOUNT_TYPES = (
        (DEPOSIT, 'Deposit account'),
        (OTHER, 'Savings account'),
        (OTHER, 'Other'),
    )

    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    number = models.CharField(max_length=34, validators=[validate_iban], help_text='IBAN format, spaceless')
    balance = models.IntegerField()
    client = models.ForeignKey(Client)

    @property
    def pretty_number(self):
        """
        Turn a spaceless IBAN number into a regular IBAN, with a space occuring every 4 chars.
        """
        return ' '.join([self.number[i:i+4] for i in range(0, len(self.number), 4)])

    def __unicode__(self):
        return u'%s (%s) | %s EUR' % (self.pretty_number, self.type, self.balance)
