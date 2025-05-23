from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'authors'

author_api_router = SimpleRouter()
author_api_router.register(
    'api', 
    views.AuthorViewSet, 
    basename='author-api'
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/budget/new/',
        views.DashboardBudget.as_view(),
        name='dashboard_budget_new'
    ),
    path(
        'dashboard/budget/delete/',
        views.DashboardBudgetDelete.as_view(),
        name='dashboard_budget_delete'
    ),
    path(
        'dashboard/budget/<int:id>/edit/',
        views.DashboardBudget.as_view(),
        name='dashboard_budget_edit'
    ),
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
]

urlpatterns += author_api_router.urls