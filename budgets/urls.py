from django.urls import include, path

from . import views

# budgets:budget
app_name = 'budgets'

urlpatterns = [
    path('', views.home, name="home"), #budgets-home
    
    path('budgets/category/<int:category_id>/', views.category, name="category"),
    path('budgets/<int:id>/', views.budget, name="budget"), #budgets-budget
]
