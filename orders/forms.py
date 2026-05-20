from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "postal_code",
            "payment_method",
        )
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "payment_method": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "payment_method":
                field.widget.attrs.update({"class": "form-control"})
