from rest_framework import serializers

from services.order.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'product_name', 'total_discount', 'total_amount', 'currency', 'status']

    @staticmethod
    def get_customer_name(obj):
        return obj.customer.full_name

    @staticmethod
    def get_product_name(obj):
        return obj.product.name
