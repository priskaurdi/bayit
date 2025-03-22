from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.budget_form import AuthorBudgetForm
from budgets.models import Budget


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardBudget(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_budget(self, id=None):
        budget = None

        if id is not None:
            budget = Budget.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not budget:
                raise Http404()

        return budget

    def render_budget(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_budget.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        budget = self.get_budget(id)
        form = AuthorBudgetForm(instance=budget)
        return self.render_budget(form)

    def post(self, request, id=None):
        budget = self.get_budget(id)
        form = AuthorBudgetForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=budget
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            budget = form.save(commit=False)

            budget.author = request.user
            budget.preparation_steps_is_html = False
            budget.is_published = False

            budget.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(
                reverse(
                    'authors:dashboard_budget_edit', args=(
                        budget.id,
                    )
                )
            )

        return self.render_budget(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardBudgetDelete(DashboardBudget):
    def post(self, *args, **kwargs):
        budget = self.get_budget(self.request.POST.get('id'))
        budget.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))