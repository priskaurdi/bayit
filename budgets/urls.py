from django.urls import include, path

from . import views

# budgets:budget
app_name = 'budgets'

urlpatterns = [
    path('', views.BudgetListViewHome.as_view(), name="home"), #budgets-home
    path('budgets/search/', views.BudgetListViewSearch.as_view(), name="search"), 
    path('budgets/category/<int:category_id>/', views.BudgetListViewCategory.as_view(), name="category"),
    path('budgets/<int:pk>/', views.BudgetDetail.as_view(), name="budget"), #budgets-budget
    
]
