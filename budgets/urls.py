from django.urls import path

from budgets.views import contato, home, sobre

urlpatterns = [
    path('/', home),
    path('sobre/', sobre),
    path('contato/', contato)
]
