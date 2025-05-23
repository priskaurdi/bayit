from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from budgets.tests.test_budget_base import BudgetMixin


class BudgetAPIv2Test(test.APITestCase, BudgetMixin):
    def get_budget_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('budgets:budgets-api-list')
        return api_url
    
    def get_budget_api_list(self):
        api_url = reverse('budgets:budgets-api-list')
        response = self.client.get(api_url)
        return response

    def get_jwt_access_token(self):
        userdata = {
            'username': 'user',
            'password': 'password'
        }
        self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        response = self.client.post(
            reverse('budgets:token_obtain_pair'), data={**userdata}
        )
        return response.data.get('access')
    
    def get_budget_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': '1',
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps.'
        }
    
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

    @patch('budgets.views.api.BudgetAPIv2Pagination.page_size', new=10)
    def test_budget_api_list_loads_budgets_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Creates 10 budgets
        budgets = self.make_budget_in_batch(qtd=10)

        # Change all budgets to the wanted category
        for budget in budgets:
            budget.category = category_wanted
            budget.save()

        # Change one budget to the NOT wanted category
        # As a result, this budget should NOT show in the page
        budgets[0].category = category_not_wanted
        budgets[0].save()

        # Action: get budgets by wanted category_id
        api_url = reverse('budgets:budgets-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_budget_api_list(reverse_result=api_url)

        # We should only see budgets from the wanted category
        self.assertEqual(
            len(response.data.get('results')),
            9
        )
    
    def test_budget_api_list_user_must_send_jwt_token_to_create_budget(self):
        api_url = self.get_budget_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_budget_api_list_logged_user_can_create_a_budget(self):
        data = self.get_budget_raw_data()
        response = self.client.post(
            self.get_budget_reverse_url(),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        )

        self.assertEqual(
            response.status_code,
            201
        )