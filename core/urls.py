from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    CashflowRecordViewSet,
)

app_name = 'core'

router = DefaultRouter()

# Регистрация справочников
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'types', TypeViewSet, basename='types')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')

# Регистрация записей ДДС
router.register(r'records', CashflowRecordViewSet, basename='records')

urlpatterns = [
    path('', include(router.urls)),
]
