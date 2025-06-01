from django import forms
from .models import CashflowRecord
from .validators import validate_cashflow_data


class CashflowRecordAdminForm(forms.ModelForm):
    class Meta:
        model = CashflowRecord
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return validate_cashflow_data(cleaned_data, context='form',
                                      form_instance=self)
