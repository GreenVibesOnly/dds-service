from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda _: redirect('core:records-list')),  # переадресация на записи
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
