from rest_framework.serializers import ModelSerializer

from .models import Status, Type, Category, SubCategory, CashflowRecord
from .validators import validate_cashflow_data


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


# Сериализатор для записи ДДС с серверной валидацией
class CashflowRecordSerializer(ModelSerializer):
    class Meta:
        model = CashflowRecord
        fields = '__all__'

    def validate(self, data):
        return validate_cashflow_data(data, context='serializer')
