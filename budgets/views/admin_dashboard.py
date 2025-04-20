from django.contrib.admin.sites import site
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncMonth

from budgets.models import Budget


@staff_member_required
def budget_dashboard(request):
    # Orçamentos por mês
    budgets_by_month = (
        Budget.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    labels_month = [b['month'].strftime('%Y-%m') for b in budgets_by_month]
    data_month = [b['count'] for b in budgets_by_month]

    # Por categoria
    budgets_by_category = (
        Budget.objects
        .values('category__name')
        .annotate(count=Count('id'))
    )
    labels_category = [b['category__name'] for b in budgets_by_category]
    data_category = [b['count'] for b in budgets_by_category]

    # Por tipo de serviço
    budgets_by_service = (
        Budget.objects
        .values('service_type')
        .annotate(count=Count('id'))
    )
    labels_service = [b['service_type'] for b in budgets_by_service]
    data_service = [b['count'] for b in budgets_by_service]

    # Por autor (usuário)
    budgets_by_authors = (
        Budget.objects
        .values('author__username')  # <- importante!
        .annotate(count=Count('id'))
    )
    labels_author = [b['author__username'] for b in budgets_by_authors]
    data_author = [b['count'] for b in budgets_by_authors]

    return site.index(request, extra_context={
        'labels_month': labels_month,
        'data_month': data_month,
        'labels_category': labels_category,
        'data_category': data_category,
        'labels_service': labels_service,
        'data_service': data_service,
        'labels_author': labels_author,
        'data_author': data_author,
    })
