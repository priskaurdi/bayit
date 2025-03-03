from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_budget_base import BudgetTestBase


class BudgetModelTest(BudgetTestBase):
    def setUp(self) -> None:
        self.budget = self.make_budget()
        return super().setUp()

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