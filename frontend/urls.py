from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CashflowRecordViewSet,
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
)

app_name = 'frontend'

router = DefaultRouter()
router.register(r'records', CashflowRecordViewSet, basename='records')
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'types', TypeViewSet, basename='types')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')

urlpatterns = [
    path('', include(router.urls)),
]
