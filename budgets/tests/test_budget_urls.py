from django.test import TestCase
from django.urls import reverse


class BudgetURLsTest(TestCase):
    def test_budget_home_url_is_correct(self):
        home_url = reverse('budgets:home')
        self.assertEqual(home_url, '/')

    def test_budget_category_url_is_correct(self):
        url = reverse('budgets:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/budgets/category/1/')

    def test_budget_detail_url_is_correct(self):
        url = reverse('budgets:budget', kwargs={'pk': 1})
        self.assertEqual(url, '/budgets/1/')
    
    def test_budget_search_url_is_correct(self):
        url = reverse('budgets:search')
        self.assertEqual(url, '/budgets/search/')
