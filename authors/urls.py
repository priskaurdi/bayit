from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/budget/new/',
        views.dashboard_budget_new,
        name='dashboard_budget_new'
    ),
    path(
        'dashboard/budget/delete/',
        views.dashboard_budget_delete,
        name='dashboard_budget_delete'
    ),
    path(
        'dashboard/budget/<int:id>/edit/',
        views.dashboard_budget_edit,
        name='dashboard_budget_edit'
    ),
]