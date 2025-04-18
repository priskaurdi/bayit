from django.urls import path

from .views import site

# budgets:budget
app_name = 'budgets'

urlpatterns = [
    path( #budgets-home
        '', 
        site.BudgetListViewHome.as_view(), 
        name="home"
    ), 
    path( #budgets-search
        'budgets/search/', 
        site.BudgetListViewSearch.as_view(), 
        name="search"
    ),
    path(
        'budgets/tags/<slug:slug>/',
        site.BudgetListViewTag.as_view(),
        name="tag"
    ),
    path( #budgets-category
        'budgets/category/<int:category_id>/', 
        site.BudgetListViewCategory.as_view(), 
        name="category"
    ),
    path( #budgets-budget
        'budgets/<int:pk>/', 
        site.BudgetDetail.as_view(), 
        name="budget"
    ), 
    path( #budgets-api
        'budgets/api/v1/',
        site.BudgetListViewHomeApi.as_view(),
        name="budgets_api_v1",
    ),
    path( #budgets-api-detail
        'budgets/api/v1/<int:pk>/',
        site.BudgetDetailAPI.as_view(),
        name="budgets_api_v1_detail",
    ),
    path( #budgets-theory
        'budgets/theory/',
        site.theory,
        name='theory',
    )
    
]
