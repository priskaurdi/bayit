from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.urls import path

from budgets.views.admin_dashboard import budget_dashboard
from tag.models import Tag

from .models import Budget, Category


class CategoryAdmin(admin.ModelAdmin):
    ...



@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_link = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }

    change_list_template = "budgets/partials/change_list.html"
    
    def changelist_view(self, request, extra_context=None):
        # Dados para gráficos
        budgets_by_month = (
            Budget.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        labels_month = [b['month'].strftime('%Y-%m') for b in budgets_by_month]
        data_month = [b['count'] for b in budgets_by_month]

        budgets_by_category = (
            Budget.objects
            .values('category__name')
            .annotate(count=Count('id'))
        )
        labels_category = [b['category__name'] for b in budgets_by_category]
        data_category = [b['count'] for b in budgets_by_category]

        budgets_by_service = (
            Budget.objects
            .values('service_type')
            .annotate(count=Count('id'))
        )
        labels_service = [b['service_type'] for b in budgets_by_service]
        data_service = [b['count'] for b in budgets_by_service]

        extra_context = extra_context or {}
        extra_context.update({
            'labels_month': labels_month,
            'data_month': data_month,
            'labels_category': labels_category,
            'data_category': data_category,
            'labels_service': labels_service,
            'data_service': data_service,
        })

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(budget_dashboard), name='budget-dashboard'),
        ]
        return custom_urls + urls

    

admin.site.register(Category, CategoryAdmin)