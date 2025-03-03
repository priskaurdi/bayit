from django.test import TestCase

from budgets.models import Budget, Category, User


class BudgetTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

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
        equipment_btus='BTUs',
        preparation_time=10,
        preparation_steps='Budget Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
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
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )