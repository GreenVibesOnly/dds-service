from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import CashflowRecordFilter
from .forms import (StatusForm, TypeForm, CategoryForm,
                    SubCategoryForm, CashflowRecordForm)
from .models import Status, Type, Category, SubCategory, CashflowRecord
from .serializers import (StatusSerializer, TypeSerializer,
                          CategorySerializer, SubCategorySerializer,
                          CashflowRecordSerializer)


# Базовый ViewSet для справочников с HTML и API-интерфейсом
class BaseReferenceViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'references/reference_list.html'
    model_name = ''
    form_class = None
    template_form = 'references/reference_form.html'
    template_confirm_delete = 'references/reference_confirm_delete.html'

    # Отображение списка объектов справочника
    def list(self, request, *args, **kwargs):
        return Response({
            'objects': self.get_queryset(),
            'model_name': self.model_name
        })

    # Страница создания нового объекта
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

    # Страница редактирования объекта
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

    # Страница подтверждения и удаления объекта
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


# Mixin с данными о справочниках для записей ДДС
class CategoryDataMixin:
    def get_category_data(self):
        return {
            'type_categories': list(Category.objects.values(
                'id', 'name', 'type_id')),
            'category_subcategories': list(SubCategory.objects.values(
                'id', 'name', 'category_id')),
        }


# ViewSet для записей ДДС с поддержкой HTML и фильтрации
class CashflowRecordViewSet(CategoryDataMixin, ModelViewSet):
    queryset = CashflowRecord.objects.select_related(
        'type', 'status', 'category', 'subcategory'
    ).all()
    serializer_class = CashflowRecordSerializer
    renderer_classes = [TemplateHTMLRenderer]
    model_name = 'Запись ДДС'
    template_name = 'records/record_list.html'
    template_form = 'records/record_form.html'
    template_confirm_delete = 'records/record_confirm_delete.html'
    form_class = CashflowRecordForm
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashflowRecordFilter

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        return Response({
            'records': qs.order_by('-created_at'),
            'request': request,
            'model_name': self.model_name,
            'status_list': Status.objects.all(),
            'type_list': Type.objects.all(),
            'category_list': Category.objects.all(),
            'subcategory_list': SubCategory.objects.all(),
        }, template_name=self.template_name)

    @action(detail=False, methods=['get', 'post'], url_path='create')
    def create_view(self, request):
        form = self.form_class(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('core:records-list')

        return Response({
            'form': form,
            'model_name': self.model_name,
            **self.get_category_data(),
        }, template_name=self.template_form)

    @action(detail=True, methods=['get', 'post'], url_path='edit')
    def edit_view(self, request, pk=None):
        obj = self.get_object()
        form = self.form_class(request.POST or None, instance=obj)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('core:records-list')

        return Response({
            'form': form,
            'model_name': self.model_name,
            **self.get_category_data(),
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
