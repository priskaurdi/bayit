from django.test import TestCase
from django.urls import resolve, reverse

from budgets import views

# Create your tests here.

class BudgetURLsTest(TestCase):
    def test_budget_home_url_is_correct(self):
        home_url = reverse('budgets:home')
        self.assertEqual(home_url, '/')

    def test_budget_category_url_is_correct(self):
        url = reverse('budgets:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/budgets/category/1/')

    def test_budget_detail_url_is_correct(self):
        url = reverse('budgets:budget', kwargs={'id': 1})
        self.assertEqual(url, '/budgets/1/')

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