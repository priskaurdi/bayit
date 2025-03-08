from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_budget_base import Budget, BudgetTestBase


class BudgetModelTest(BudgetTestBase):
    def setUp(self) -> None:
        self.budget = self.make_budget()
        return super().setUp()

    def make_budget_no_defaults(self):
        budget = Budget(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Budget Title',
            description='Budget Description',
            slug='budget-slug-for-no-defaults',
            service_type='limpeza',  # Corrigido: Adicionado valor obrigatório
            scheduled_date='2025-03-10',  # Corrigido: Adicionado valor obrigatório
            scheduled_time='10:00',  # Corrigido: Adicionado valor obrigatório
            street='Rua Exemplo',  # Corrigido: Adicionado valor obrigatório
            number='123',  # Corrigido: Adicionado valor obrigatório
            neighborhood='Bairro Teste',  # Corrigido: Adicionado valor obrigatório
            city='Cidade Teste',  # Corrigido: Adicionado valor obrigatório
            state='SP',  # Corrigido: Adicionado valor obrigatório
            zipcode='12345-678',  # Corrigido: Adicionado valor obrigatório
            equipment_brand='Marca',
            equipment_model='Modelo',
            equipment_btus=9000,
            budget_detail='Detalhes do orçamento',  # Corrigido: Adicionado valor obrigatório
            servings=2,  # Corrigido: Adicionado valor obrigatório
            servings_unit='Porções',  # Corrigido: Adicionado valor obrigatório
            preparation_time=10,
            preparation_time_unit='consultorios',
            preparation_steps='Budget Preparation Steps',
            is_published=False
        )
        budget.full_clean()
        budget.save()
        return budget
    
    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_budget_fields_max_length(self, field, max_length):
        setattr(self.budget, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.budget.full_clean()
    
    def test_budget_preparation_steps_is_html_is_false_by_default(self):
        budget = self.make_budget_no_defaults()
        self.assertFalse(
            budget.preparation_steps_is_html,
            msg='Budget preparation_steps_is_html is not False',
        )

    def test_budget_is_published_is_false_by_default(self):
        budget = self.make_budget_no_defaults()
        self.assertFalse(
            budget.is_published,
            msg='Budget is_published is not False',
        )

    def test_budget_string_representation(self):
        needed = 'Testing Representation'
        self.budget = self.make_budget(  # Garantindo que os campos obrigatórios sejam passados
            title=needed,
            service_type='Instalação',  # Adicionado para evitar erro
            budget_detail='Orçamento teste',  # Adicionado para evitar erro
        )
        self.budget.full_clean()
        self.budget.save()
        self.assertEqual(
            str(self.budget), needed,
            msg=f'Budget string representation must be "{needed}" but "{str(self.budget)}" was received.'
        )
