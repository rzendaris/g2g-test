from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', _('Order Pending')
    PAID = 'PAID', _('Order Paid')
    DELIVERED = 'DELIVERED', _('Order Delivered')


class RedemptionPointReference(models.TextChoices):
    ORDER = 'ORDER', _('Order')
