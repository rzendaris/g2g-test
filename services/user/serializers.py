from rest_framework import serializers

from services.order.functions import calculate_reward_point
from services.user.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    point = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'point']

    @staticmethod
    def get_point(obj):
        point = calculate_reward_point(obj)
        return point
