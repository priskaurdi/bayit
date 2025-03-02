from django.test import TestCase
from django.urls import resolve, reverse

from budgets import views

# Create your tests here.


class BudgetViewsTest(TestCase):
    def test_budget_home_view_function_is_correct(self):
        view = resolve(reverse('budgets:home'))
        self.assertIs(view.func, views.home)

    def test_budget_category_view_function_is_correct(self):
        view = resolve(
            reverse('budgets:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_budget_detail_view_function_is_correct(self):
        view = resolve(
            reverse('budgets:budget', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.budget)