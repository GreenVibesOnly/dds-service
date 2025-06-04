from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import CashflowRecordFilter
from .forms import (StatusForm, TypeForm, CategoryForm,
                    SubCategoryForm, CashflowRecordAdminForm)
from .models import Status, Type, Category, SubCategory, CashflowRecord
from .serializers import (StatusSerializer, TypeSerializer,
                          CategorySerializer, SubCategorySerializer,
                          CashflowRecordSerializer)


class BaseReferenceViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'references/reference_list.html'
    model_name = ''
    form_class = None
    template_form = 'references/reference_form.html'
    template_confirm_delete = 'references/reference_confirm_delete.html'

    def list(self, request, *args, **kwargs):
        return Response({
            'objects': self.get_queryset(),
            'model_name': self.model_name
        })

    @action(detail=False, methods=['get', 'post'], url_path='create')
    def create_view(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(request.path.rsplit('/', 2)[0] + '/')
        else:
            form = self.form_class()
        return Response({'form': form, 'model_name': self.model_name},
                        template_name=self.template_form)

    @action(detail=True, methods=['get', 'post'], url_path='edit')
    def edit_view(self, request, pk=None):
        obj = self.get_object()
        if request.method == 'POST':
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('../../')
        else:
            form = self.form_class(instance=obj)
        return Response({'form': form, 'model_name': self.model_name},
                        template_name=self.template_form)

    @action(detail=True, methods=['get', 'post'], url_path='delete')
    def delete_view(self, request, pk=None):
        obj = self.get_object()
        if request.method == 'POST':
            obj.delete()
            return redirect('../../')
        return Response({'object': obj, 'model_name': self.model_name},
                        template_name=self.template_confirm_delete)


class StatusViewSet(BaseReferenceViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    form_class = StatusForm
    model_name = 'Статус'


class TypeViewSet(BaseReferenceViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    form_class = TypeForm
    model_name = 'Тип'


class CategoryViewSet(BaseReferenceViewSet):
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    form_class = CategoryForm
    model_name = 'Категория'


class SubCategoryViewSet(BaseReferenceViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    form_class = SubCategoryForm
    model_name = 'Подкатегория'


class CashflowRecordViewSet(ModelViewSet):
    queryset = CashflowRecord.objects.select_related(
        'type', 'status', 'category', 'subcategory'
    ).all()
    serializer_class = CashflowRecordSerializer
    renderer_classes = [TemplateHTMLRenderer]
    model_name = 'Запись ДДС'
    template_name = 'records/record_list.html'
    template_form = 'records/record_form.html'
    template_confirm_delete = 'records/record_confirm_delete.html'
    form_class = CashflowRecordAdminForm
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashflowRecordFilter

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        filters = {
            'created_at__gte': request.GET.get('date_after'),
            'created_at__lte': request.GET.get('date_before'),
            'status_id': request.GET.get('status'),
            'type_id': request.GET.get('type'),
            'category_id': request.GET.get('category'),
            'subcategory_id': request.GET.get('subcategory'),
        }
        filters = {k: v for k, v in filters.items() if v}
        qs = qs.filter(**filters).order_by('-created_at')

        return Response({
            'records': qs,
            'request': request,
            'model_name': self.model_name,
            'status_list': Status.objects.all(),
            'type_list': Type.objects.all(),
            'category_list': Category.objects.all(),
            'subcategory_list': SubCategory.objects.all(),
        }, template_name=self.template_name)

    @action(detail=False, methods=['get', 'post'], url_path='create')
    def create_view(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect('core:records-list')
        else:
            form = self.form_class()

        return Response({
            'form': form,
            'model_name': self.model_name,
            'type_categories': list(Category.objects.values(
                'id', 'name', 'type_id')),
            'category_subcategories': list(SubCategory.objects.values(
                'id', 'name', 'category_id')),
        }, template_name=self.template_form)

    @action(detail=True, methods=['get', 'post'], url_path='edit')
    def edit_view(self, request, pk=None):
        obj = self.get_object()
        if request.method == 'POST':
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('core:records-list')
        else:
            form = self.form_class(instance=obj)

        return Response({
            'form': form,
            'model_name': self.model_name,
            'type_categories': list(Category.objects.values(
                'id', 'name', 'type_id')),
            'category_subcategories': list(SubCategory.objects.values(
                'id', 'name', 'category_id')),
        }, template_name=self.template_form)

    @action(detail=True, methods=['get', 'post'], url_path='delete')
    def delete_view(self, request, pk=None):
        obj = self.get_object()
        if request.method == 'POST':
            obj.delete()
            return redirect('core:records-list')
        return Response({
            'object': obj,
            'model_name': self.model_name,
        }, template_name=self.template_confirm_delete)
