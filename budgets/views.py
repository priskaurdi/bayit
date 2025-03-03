from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.budgets.factory import make_budget

from .models import Budget

# Create your views here.

def home(request):
    budgets = get_list_or_404(
            Budget.objects.filter(
            is_published=True
        ).order_by('-id')
    )
    return render(request, 'budgets/pages/home.html', context={
        'budgets': budgets,
    })

def category(request, category_id):
    budgets = get_list_or_404(
            Budget.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )

    return render(request, 'budgets/pages/category.html', context={
        'budgets': budgets,
        'title': f'{budgets[0].category.name} - Category | '
    })

def budget(request, id):
    budget = get_object_or_404(Budget,
        pk=id,
        is_published=True,
    )

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
    
    return render(request, 'budgets/pages/search.html'{
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'budgets': budgets,
    })
