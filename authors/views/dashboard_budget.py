from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.budget_form import AuthorBudgetForm
from budgets.models import Budget


class DashboardBudget(View):
    

        if not budget:
            raise Http404()

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
                reverse('authors:dashboard_budget_edit', args=(id,))
            )

        return render(
            request,
            'authors/pages/dashboard_budget.html',
            context={
                'form': form
            }
        )