from django.urls import resolve, reverse

from budgets import views

from .test_budget_base import BudgetTestBase


class BudgetDetailViewTest(BudgetTestBase):
    def test_budget_detail_view_function_is_correct(self):
        view = resolve(
            reverse('budgets:budget', kwargs={'id': 1})
        )
        self.assertIs(view.func.view_class, views.BudgetDetail)

    def test_budget_detail_view_returns_404_if_no_budgets_found(self):
        response = self.client.get(
            reverse('budgets:budget', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_budget_detail_template_loads_the_correct_budget(self):
        needed_title = 'This is a detail page - It load one budget'

        # Need a budget for this test
        self.make_budget(title=needed_title)

        response = self.client.get(
            reverse(
                'budgets:budget',
                kwargs={
                    'pk': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # Check if one budget exists
        self.assertIn(needed_title, content)

    def test_budget_detail_template_dont_load_budget_not_published(self):
        """Test budget is_published False dont show"""
        # Need a budget for this test
        budget = self.make_budget(is_published=False)

        response = self.client.get(
            reverse(
                'budgets:budget',
                kwargs={
                    'pk': budget.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)