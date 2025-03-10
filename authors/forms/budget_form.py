from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from authors.validators import AuthorBudgetValidator
from budgets.models import Budget
from utils.django_forms import add_attr


class AuthorBudgetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Budget
        fields = [
            'title', 'description', 'slug', 'equipment_brand', 'equipment_model',
            'equipment_btus', 'preparation_time', 'preparation_time_unit',
            'preparation_steps', 'preparation_steps_is_html', 'scheduled_date',
            'scheduled_time', 'is_published', 'cover'
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Cômodo', 'Cômodo'),
                    ('Salão', 'Salão'),
                    ('Sala', 'Sala'),
                    ('Consultório', 'Consultório'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Dias', 'Dias'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorBudgetValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean