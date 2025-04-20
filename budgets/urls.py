from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from budgets import views

# budgets:budget
app_name = 'budgets'

budget_api_v2_router = SimpleRouter()
budget_api_v2_router.register(
    'budgets/api/v2',
    views.BudgetAPIv2ViewSet,
    basename='budgets-api',
)

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
    ),
    
    path(
        'budgets/api/v2/tag/<int:pk>/',
        views.tag_api_detail,
        name='budgets_api_v2_tag',
    ),
    path(
        'budgets/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'budgets/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'budgets/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    # Por último
    path('', include(budget_api_v2_router.urls)),
]
