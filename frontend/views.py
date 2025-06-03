from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.forms import (StatusForm, TypeForm, CategoryForm,
                       SubCategoryForm, CashflowRecordAdminForm)
from api.models import Status, Type, Category, SubCategory, CashflowRecord
from api.serializers import (StatusSerializer, TypeSerializer,
                             CategorySerializer, SubCategorySerializer,
                             CashflowRecordSerializer)


class BaseReferenceViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reference_list.html'
    model_name = ''
    form_class = None
    template_form = 'reference_form.html'
    template_confirm_delete = 'reference_confirm_delete.html'

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


class CashflowRecordViewSet(BaseReferenceViewSet):
    queryset = CashflowRecord.objects.select_related(
        'type', 'status', 'category', 'subcategory'
    ).all()
    serializer_class = CashflowRecordSerializer
    form_class = CashflowRecordAdminForm
    model_name = 'Запись ДДС'
    template_name = 'record_list.html'
    template_form = 'record_form.html'
    template_confirm_delete = 'record_confirm_delete.html'

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        # Фильтрация через GET-параметры
        filters = {
            'created_at__gte': request.GET.get('date_after'),
            'created_at__lte': request.GET.get('date_before'),
            'status__name__icontains': request.GET.get('status'),
            'category__name__icontains': request.GET.get('category'),
            'subcategory__name__icontains': request.GET.get('subcategory'),
        }
        filters = {k: v for k, v in filters.items() if v}
        qs = qs.filter(**filters)

        return Response({
            'records': qs,
            'model_name': self.model_name,
            'request': request  # чтобы использовать значения фильтра в шаблоне
        })