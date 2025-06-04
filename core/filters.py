from django_filters import rest_framework as filters
from .models import CashflowRecord, Status, Type, Category, SubCategory


# Фильтрация записей по дате, статусу, типу, категории и подкатегории
class CashflowRecordFilter(filters.FilterSet):
    date_after = filters.DateFilter(field_name='created_at',
                                    lookup_expr='gte')
    date_before = filters.DateFilter(field_name='created_at',
                                     lookup_expr='lte')
    status = filters.ModelChoiceFilter(queryset=Status.objects.all())
    type = filters.ModelChoiceFilter(queryset=Type.objects.all())
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    subcategory = filters.ModelChoiceFilter(queryset=SubCategory.objects.all())

    class Meta:
        model = CashflowRecord
        fields = ['status', 'type', 'category', 'subcategory']
