from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    CashflowRecordViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'records', CashflowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
