from django import forms
from CISCO_DNAC_APP.models import *


class AddControllerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = DnacControllers
        fields = '__all__'
