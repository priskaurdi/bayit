from django.urls import path

from . import views

# budgets:budget
app_name = 'budgets'

urlpatterns = [
    path( #budgets-home
        '', 
        views.BudgetListViewHome.as_view(), 
        name="home"
    ), 
    path( #budgets-search
        'budgets/search/', 
        views.BudgetListViewSearch.as_view(), 
        name="search"
    ),
    path(
        'budgets/tags/<slug:slug>/',
        views.BudgetListViewTag.as_view(),
        name="tag"
    ),
    path( #budgets-category
        'budgets/category/<int:category_id>/', 
        views.BudgetListViewCategory.as_view(), 
        name="category"
    ),
    path( #budgets-budget
        'budgets/<int:pk>/', 
        views.BudgetDetail.as_view(), 
        name="budget"
    ), 
    path( #budgets-api
        'budgets/api/v1/',
        views.BudgetListViewHomeApi.as_view(),
        name="budgets_api_v1",
    ),
    path( #budgets-api-detail
        'budgets/api/v1/<int:pk>/',
        views.BudgetDetailAPI.as_view(),
        name="budgets_api_v1_detail",
    ),
    path( #budgets-theory
        'budgets/theory/',
        views.theory,
        name='theory',
    )
    
]
