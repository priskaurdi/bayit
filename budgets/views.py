#from django.http import HttpResponse
from django.shortcuts import render

from utils.budgets.factory import make_budget

# Create your views here.

def home(request):
    return render(request, 'budgets/pages/home.html', context={
        'budgets': [make_budget() for _ in range(10)],
    })

def budget(request, id):
    return render(request, 'budgets/pages/budget-view.html', context={
        'budget': make_budget(),
        'is_detail_page': True,
    })
