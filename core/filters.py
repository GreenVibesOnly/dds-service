from django_filters import rest_framework as filters
from .models import CashflowRecord


class CashflowRecordFilter(filters.FilterSet):
    date_after = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = filters.DateFilter(field_name='date', lookup_expr='lte')

    status = filters.CharFilter(field_name='status__name',
                                lookup_expr='icontains')
    type = filters.CharFilter(field_name='type__name',
                              lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name',
                                  lookup_expr='icontains')
    subcategory = filters.CharFilter(field_name='subcategory__name',
                                     lookup_expr='icontains')

    class Meta:
        model = CashflowRecord
        fields = []
