from django.urls import path
from .views import record_list_view, record_create_view

app_name = 'frontend'

urlpatterns = [
    path('', record_list_view, name='record_list'),
    path('create/', record_create_view, name='create'),
]
