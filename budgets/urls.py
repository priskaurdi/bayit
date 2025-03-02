from django.urls import path

from budgets.views import home

urlpatterns = [
    path('/', home),
]
