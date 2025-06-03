from django import forms
from .models import CashflowRecord, Status, Type, Category, SubCategory
from .validators import validate_cashflow_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']


class CashflowRecordAdminForm(forms.ModelForm):
    class Meta:
        model = CashflowRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'
        self.fields['created_at'].widget.input_type = 'date'

    def clean(self):
        cleaned_data = super().clean()
        return validate_cashflow_data(cleaned_data, context='form',
                                      form_instance=self)
