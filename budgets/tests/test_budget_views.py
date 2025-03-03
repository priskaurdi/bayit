from django.test import TestCase
from django.urls import resolve, reverse

from budgets import views

from .test_budget_base import BudgetTestBase

# Create your tests here.

class BudgetViewsTest(BudgetTestBase):
    def test_budget_home_view_function_is_correct(self):
        view = resolve(reverse('budgets:home'))
        self.assertIs(view.func, views.home)

    def test_budget_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertEqual(response.status_code, 200)

    def test_budget_home_view_loads_correct_template(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertTemplateUsed(response, 'budgets/pages/home.html')
    
    def test_budget_home_template_shows_no_budgets_found_if_no_budgets(self):
        response = self.client.get(reverse('budgets:home'))
        self.assertIn(
            '<h1>No budgets found here 🥲</h1>',
            response.content.decode('utf-8')
        )

        # Tenho que revisar mais algumas coisas sobre o test
        self.fail('Para que eu possa entender onde to errando')

    
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
            '<h1>No budgets found here 🥲</h1>',
            response.content.decode('utf-8')
        )

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

    def test_budget_detail_view_function_is_correct(self):
        view = resolve(
            reverse('budgets:budget', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.budget)
    
    def test_budget_detail_view_returns_404_if_no_budgets_found(self):
        response = self.client.get(
            reverse('budgets:budget', kwargs={'id': 1000})
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
                    'id': 1
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
            reverse('budgets:budget', kwargs={'id': budget.id})
        )

        self.assertEqual(response.status_code, 404)