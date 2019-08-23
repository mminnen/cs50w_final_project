from django import forms
from CISCO_DNAC_APP.models import *


class AddControllerForm(forms.ModelForm):

    class Meta:
        model = DnacControllers
        fields = '__all__'
