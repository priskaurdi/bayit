from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from budgets.tests.test_budget_base import BudgetMixin


class BudgetAPIv2Test(test.APITestCase, BudgetMixin):
    def get_budget_api_list(self):
        api_url = reverse('budgets:budgets-api-list')
        response = self.client.get(api_url)
        return response

    def test_budget_api_list_returns_status_code_200(self):
        response = self.get_budget_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('budgets.views.api.BudgetAPIv2Pagination.page_size', new=7)
    def test_budget_api_list_loads_correct_number_of_budgets(self):
        wanted_number_of_budgets = 7
        self.make_budget_in_batch(qtd=wanted_number_of_budgets)

        response = self.client.get(
            reverse('budgets:budgets-api-list') + '?page=1'
        )
        qtd_of_loaded_budgets = len(response.data.get('results'))

        self.assertEqual(
            wanted_number_of_budgets,
            qtd_of_loaded_budgets
        )

    def test_budget_api_list_do_not_show_not_published_budgets(self):
        budgets = self.make_budget_in_batch(qtd=2)
        budget_not_published = budgets[0]
        budget_not_published.is_published = False
        budget_not_published.save()
        response = self.get_budget_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )