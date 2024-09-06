from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from services.order.forms import CreateOrderForm
from services.order.functions import create_order
from services.order.serializers import OrderSerializer
from services.user.helpers import form_error_response, generate_response


class OrderView(APIView):
    allowed_methods = ('POST', )
    permission_classes = (AllowAny,)

    def post(self, request):
        form = CreateOrderForm(request.POST)

        if form.is_valid():
            order_created = create_order(form.cleaned_data)
            serializer = OrderSerializer(order_created, context={'request': request}).data

            return generate_response(serializer)
        else:
            return form_error_response(form)
