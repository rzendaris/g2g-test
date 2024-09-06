from django import forms

from services.order.models import Product
from services.user.models import Customer


class CreateOrderForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.CharField(required=True, validators=[self.email_validator])
        self.fields['product_id'] = forms.CharField(required=True, validators=[self.product_validator])

    def email_validator(self, email):
        customer = Customer.objects.filter(email=email).first()
        if customer is None:
            raise forms.ValidationError("Customer Not found")

    def product_validator(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            raise forms.ValidationError("Product Not found")
