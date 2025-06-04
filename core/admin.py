from django.contrib import admin

from .forms import CashflowRecordAdminForm
from .models import (
    Status,
    Type,
    Category,
    SubCategory,
    CashflowRecord,
)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(CashflowRecord)
class CashflowRecordAdmin(admin.ModelAdmin):
    form = CashflowRecordAdminForm
    list_display = [
        'created_at', 'type', 'status', 'category',
        'subcategory', 'amount', 'comment'
    ]
    list_filter = ['type', 'status', 'category', 'subcategory', 'created_at']
    search_fields = ['comment']
    created_at_hierarchy = 'created_at'
    ordering = ['-created_at']
