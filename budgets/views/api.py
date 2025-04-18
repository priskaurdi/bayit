from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Budget
from ..serializers import BudgetSerializer, TagSerializer


@api_view()
def budget_api_list(request):
    budgets = Budget.objects.get_published()[:10]
    serializer = BudgetSerializer(
        instance=budgets,
        many=True,
        context={'request': request},
    )
    return Response(serializer.data)


@api_view()
def budget_api_detail(request, pk):
    budget = get_object_or_404(
        Budget.objects.get_published(),
        pk=pk
    )
    serializer = BudgetSerializer(
        instance=budget,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)