from django.db import models
from django.utils.translation import ugettext_lazy as _

from services.order.constants import OrderStatus
from services.user.models import TimeStampedModel, Customer


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, blank=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return "{0}".format(self.name)


class Order(TimeStampedModel):

    customer = models.ForeignKey(
        Customer,
        verbose_name=_('Customer'),
        related_name='customer_order',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='product_order',
        on_delete=models.CASCADE
    )
    currency = models.CharField(max_length=3, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return "{0} - {1}".format(self.customer.full_name, self.product.name)
