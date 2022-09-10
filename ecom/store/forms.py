from django import forms

PAYMENT_CHOICES = (
    ('Card', 'Credit Card'),
    ('COD', 'Cash on Delivery')
)


class CheckoutForm(forms.Form):

    address1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main Building'
    }))
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or Suite'
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Country'
    }))
    zip_code = forms.CharField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class PaymentForm(forms.Form):
    card_owner = forms.CharField(max_length=200)
    card_number = forms.CharField(max_length=16)
    cvv = forms.CharField(max_length=3)
