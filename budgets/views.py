import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

#from utils.budgets.factory import make_budget
from utils.pagination import make_pagination

from .models import Budget

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def home(request):
    budgets = Budget.objects.filter(
            is_published=True
        ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, budgets, PER_PAGE)
    return render(request, 'budgets/pages/home.html', context={
        'budgets': page_obj,
        'pagination_range': pagination_range      
    })

def category(request, category_id):
    budgets = get_list_or_404(
            Budget.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request, budgets, PER_PAGE)
    return render(request, 'budgets/pages/category.html', context={
        'budgets': page_obj,
        'pagination_range': pagination_range,
        'title': f'{budgets[0].category.name} - Category | '
    })

def budget(request, id):
    budget = get_object_or_404(Budget, pk=id, is_published=True,)

    return render(request, 'budgets/pages/budget-view.html', context={
        'budget': budget,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    budgets = Budget.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, budgets, PER_PAGE)
    return render(request, 'budgets/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'budgets': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
