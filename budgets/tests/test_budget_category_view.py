from django.urls import resolve, reverse

from budgets import views

from .test_budget_base import BudgetTestBase


class BudgetCategoryViewTest(BudgetTestBase):
    def test_budget_category_view_function_is_correct(self):
        view = resolve(
            reverse('budgets:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_budget_category_view_returns_404_if_no_budgets_found(self):
        response = self.client.get(
            reverse('budgets:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_budget_category_template_loads_budgets(self):
        needed_title = 'This is a category test'
        # Need a budget for this test
        self.make_budget(title=needed_title)

        response = self.client.get(reverse('budgets:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one budget exists
        self.assertIn(needed_title, content)

    def test_budget_category_template_dont_load_budgets_not_published(self):
        """Test budget is_published False dont show"""
        # Need a budget for this test
        budget = self.make_budget(is_published=False)

        response = self.client.get(
            reverse('budgets:budget', kwargs={'id': budget.category.id})
        )

        self.assertEqual(response.status_code, 404)