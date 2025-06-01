from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import CashflowRecordFilter
from .models import Status, Type, Category, SubCategory, CashflowRecord
from .serializers import (
    StatusSerializer,
    TypeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    CashflowRecordSerializer
)


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class CashflowRecordViewSet(ModelViewSet):
    queryset = CashflowRecord.objects.all()
    serializer_class = CashflowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashflowRecordFilter
