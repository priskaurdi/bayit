#from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from utils.budgets.factory import make_budget

from .models import Budget

# Create your views here.

def home(request):
    budgets = Budget.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'budgets/pages/home.html', context={
        'budgets': budgets,
    })

def category(request, category_id):
    budgets = Budget.objects.filter(
        category__id=category_id, 
        is_published=True
    ).order_by('-id')

    if not budgets:
        raise Http404('Not found 🥲')
    
    return render(request, 'budgets/pages/category.html', context={
        'budgets': budgets,
        'title': f'{budgets.first().category.name} - Category | '
    })

def budget(request, id):
    return render(request, 'budgets/pages/budget-view.html', context={
        'budget': make_budget(),
        'is_detail_page': True,
    })
