from django.shortcuts import render, redirect

from api.models import CashflowRecord
from api.forms import CashflowRecordAdminForm


def record_list_view(request):
    qs = CashflowRecord.objects.select_related(
        'type', 'status', 'category', 'subcategory').all()

    date_after = request.GET.get('date_after')
    date_before = request.GET.get('date_before')
    status = request.GET.get('status')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    if date_after:
        qs = qs.filter(date__gte=date_after)
    if date_before:
        qs = qs.filter(date__lte=date_before)
    if status:
        qs = qs.filter(status__name__icontains=status)
    if category:
        qs = qs.filter(category__name__icontains=category)
    if subcategory:
        qs = qs.filter(subcategory__name__icontains=subcategory)

    return render(request, "record_list.html", {"records": qs})


def record_create_view(request):
    if request.method == "POST":
        form = CashflowRecordAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("frontend:record_list")
    else:
        form = CashflowRecordAdminForm()
    return render(request, "record_form.html", {"form": form})
