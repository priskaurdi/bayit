from unittest.mock import patch

from django.urls import resolve, reverse

from budgets import views

from .test_budget_base import BudgetTestBase


class BudgetHomeViewTest(BudgetTestBase):
    def test_budget_home_view_function_is_correct(self):
        view = resolve(reverse('budgets:home'))
        self.assertIs(view.func.view_class, views.BudgetListViewHome)

    def test_budget_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertEqual(response.status_code, 200)

    def test_budget_home_view_loads_correct_template(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertTemplateUsed(response, 'budgets/pages/home.html')

    def test_budget_home_template_shows_no_budgets_found_if_no_budgets(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertIn(
            '<h1>No budgets found here.</h1>',
            response.content.decode('utf-8')
        )

    def test_budget_home_template_loads_budgets(self):
        # Need a budget for this test
        self.make_budget()

        response = self.client.get(reverse('budgets:home'))
        content = response.content.decode('utf-8')
        response_context_budgets = response.context['budgets']

        # Check if one budget exists
        self.assertIn('Budget Title', content)
        self.assertEqual(len(response_context_budgets), 1)

    def test_budget_home_template_dont_load_budgets_not_published(self):
        """Test budget is_published False dont show"""
        # Need a budget for this test
        self.make_budget(is_published=False)

        response = self.client.get(reverse('budgets:home'))

        # Check if one budget exists
        self.assertIn(
            '<h1>No budgets found here.</h1>',
            response.content.decode('utf-8')
        )

    def test_budget_home_is_paginated(self):
        self.make_budget_in_batch(qtd=8)

        with patch('budgets.views.PER_PAGE', new=3):
            response = self.client.get(reverse('budgets:home'))
            budgets = response.context['budgets']
            paginator = budgets.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
    
    def test_invalid_page_query_uses_page_one(self):
        self.make_budget_in_batch(qtd=8)

        with patch('budgets.views.PER_PAGE', new=3):
            response = self.client.get(reverse('budgets:home') + '?page=12A')
            self.assertEqual(
                response.context['budgets'].number,
                1
            )
            response = self.client.get(reverse('budgets:home') + '?page=2')
            self.assertEqual(
                response.context['budgets'].number,
                2
            )
            response = self.client.get(reverse('budgets:home') + '?page=3')
            self.assertEqual(
                response.context['budgets'].number,
                3
            )