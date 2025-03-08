from django.test import TestCase

from budgets.models import Budget, Category, User


class BudgetMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='aluno',
        last_name='univesp',
        username='alunounivesp',
        password='@luno123',
        email='aluno@univesp.br',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_budget(
        self,
        category_data=None,
        author_data=None,
        title='Budget Title',
        description='Budget Description',
        slug='budget-slug',
        equipment_brand='Marca',
        equipment_model='Modelo',
        equipment_btus=1500,
        preparation_time=10,
        preparation_time_unit='horas',
        preparation_steps='Budget Preparation Steps',
        preparation_steps_is_html=False,
        scheduled_date='2025-03-10',
        scheduled_time='10:00',
        is_published=True,
        street="Rua Exemplo",
        number="123",
        neighborhood="Bairro Exemplo",
        city="Cidade Exemplo",
        state="SP",
        zipcode="00000-000",
        status="Pendente",
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Budget.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            equipment_brand=equipment_brand,
            equipment_model=equipment_model,
            equipment_btus=equipment_btus,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            is_published=is_published,
            street=street,
            number=number,
            neighborhood=neighborhood,
            city=city,
            state=state,
            zipcode=zipcode,
            status=status,
        )

    
    def make_budget_in_batch(self, qtd=10):
        budgets = []
        for i in range(qtd):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            budget = self.make_budget(**kwargs)
            budgets.append(budget)
        return budgets

class BudgetTestBase(TestCase, BudgetMixin):
    def setUp(self) -> None:
        return super().setUp()