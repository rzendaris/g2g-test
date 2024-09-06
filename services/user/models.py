from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from services.order.constants import RedemptionPointReference


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField(_('Created At'))
    updated_at = AutoLastModifiedField(_('Updated At'))

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    full_name = models.CharField(max_length=255, blank=False)
    email = models.CharField(unique=True, max_length=255, blank=False)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return "{0}".format(self.full_name)


class CustomerPoint(TimeStampedModel):
    customer = models.ForeignKey(
        Customer,
        verbose_name=_('Customer'),
        related_name='customer_customer_point',
        on_delete=models.CASCADE
    )
    granted_point = models.BigIntegerField(default=0)
    used_point = models.BigIntegerField(default=0)
    expired_at = models.DateField(blank=False)

    class Meta:
        verbose_name = _('Customer Point')
        verbose_name_plural = _('Customer Points')

    def __str__(self):
        return "{0}".format(self.customer.full_name)


class CustomerPointRedemptionHistory(TimeStampedModel):
    customer_point = models.ForeignKey(
        CustomerPoint,
        verbose_name=_('Customer Point'),
        related_name='customer_point_redemption',
        on_delete=models.CASCADE
    )
    used_point = models.BigIntegerField(default=0)
    reference_name = models.CharField(
        max_length=50,
        choices=RedemptionPointReference.choices
    )
    reference_id = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = _('Customer Point Redemption')
        verbose_name_plural = _('Customer Point Redemptions')

    def __str__(self):
        return "{0} - {1}".format(self.customer_point, self.reference_name)
