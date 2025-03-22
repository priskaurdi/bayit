from django.urls import resolve, reverse

from budgets import views

from .test_budget_base import BudgetTestBase


class BudgetSearchViewTest(BudgetTestBase):
    def test_budget_search_uses_correct_view_function(self):
        resolved = resolve(reverse('budgets:search'))
        self.assertIs(resolved.func.view_class, views.BudgetListViewSearch)

    def test_budget_search_loads_correct_template(self):
        response = self.client.get(reverse('budgets:search') + '?q=teste')
        self.assertTemplateUsed(response, 'budgets/pages/search.html')

    def test_budget_search_raises_404_if_no_search_term(self):
        url = reverse('budgets:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_budget_search_term_is_on_page_title_and_escaped(self):
        url = reverse('budgets:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
    
    def test_budget_search_can_find_budget_by_title(self):
        title1 = 'This is budget one'
        title2 = 'This is budget two'

        budget1 = self.make_budget(
            title=title1, author_data={'username': 'one'}
        )
        budget2 = self.make_budget(
            title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('budgets:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(budget1, response1.context['budgets'])
        self.assertNotIn(budget2, response1.context['budgets'])

        self.assertIn(budget2, response2.context['budgets'])
        self.assertNotIn(budget1, response2.context['budgets'])

        self.assertIn(budget1, response_both.context['budgets'])
        self.assertIn(budget2, response_both.context['budgets'])