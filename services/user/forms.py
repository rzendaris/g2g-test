from django import forms

from services.user.models import Customer


class CustomerInfoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CustomerInfoForm, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.CharField(required=True, validators=[self.email_validator])

    def email_validator(self, email):
        customer = Customer.objects.filter(email=email).first()
        if customer is None:
            raise forms.ValidationError("Customer Not found")
