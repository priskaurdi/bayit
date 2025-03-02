from django.urls import path

from . import views

# budgets:budget
app_name = 'budgets'

urlpatterns = [
    path('/', views.home, name="budgets-home"),
    path('budgets/<int:id>/', views.budget, name="budget"), #budgets-budget
]
