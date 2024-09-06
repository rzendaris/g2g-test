from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from services.user.forms import CustomerInfoForm
from services.user.helpers import form_error_response, generate_response
from services.user.models import Customer
from services.user.serializers import CustomerSerializer


class CustomerInfoView(APIView):
    allowed_methods = ('GET', )
    permission_classes = (AllowAny,)

    def get(self, request):
        form = CustomerInfoForm(request.GET)

        if form.is_valid():
            customer = Customer.objects.filter(email=form.data['email']).first()
            serializer = CustomerSerializer(customer).data

            return generate_response(serializer)
        else:
            return form_error_response(form)
