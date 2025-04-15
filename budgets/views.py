import os

from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from tag.models import Tag
#from utils.budgets.factory import make_budget
from utils.pagination import make_pagination

from .models import Budget

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def theory(request, *args, **kwargs):
    budgets = Budget.objects.values('id', 'title')

    context = {
        'budgets': budgets
    }

    return render(
        request,
        'budgets/pages/theory.html',
        context=context
    )


class BudgetListViewBase(ListView):
    model = Budget
    context_object_name = 'budgets'
    ordering = ['-id']
    template_name = 'budgets/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category', 'author__profile')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('budgets'),
            PER_PAGE
        )
        ctx.update(
            {'budgets': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class BudgetListViewHome(BudgetListViewBase):
    template_name = 'budgets/pages/home.html'


class BudgetListViewHomeApi(BudgetListViewBase):
    template_name = 'budgets/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        budgets = self.get_context_data()['budgets']
        budgets_list = budgets.object_list.values()

        return JsonResponse(
            list(budgets_list),
            safe=False
        )


class BudgetListViewCategory(BudgetListViewBase):
    template_name = 'budgets/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("budgets")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class BudgetListViewTag(BudgetListViewBase):
    template_name = 'budgets/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No budgets found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx


class BudgetListViewSearch(BudgetListViewBase):
    template_name = 'budgets/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class BudgetDetail(DetailView):
    model = Budget
    context_object_name = 'budget'
    template_name = 'budgets/pages/budget-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx
    

class BudgetDetailAPI(BudgetDetail):
    def render_to_response(self, context, **response_kwargs):
        budget = self.get_context_data()['budget']
        budget_dict = model_to_dict(budget)

        budget_dict['created_at'] = str(budget.created_at)
        budget_dict['updated_at'] = str(budget.updated_at)

        if budget_dict.get('cover'):
            budget_dict['cover'] = self.request.build_absolute_uri() + \
                budget_dict['cover'].url[1:]
        else:
            budget_dict['cover'] = ''

        del budget_dict['is_published']
        del budget_dict['preparation_steps_is_html']

        return JsonResponse(
            budget_dict,
            safe=False,
        )