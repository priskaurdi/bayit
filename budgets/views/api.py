from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Budget
from ..serializers import BudgetSerializer, TagSerializer


@api_view(http_method_names=['get', 'post'])
def budget_api_list(request):
    if request.method == 'GET':
        budgets = Budget.objects.get_published()[:10]
        serializer = BudgetSerializer(
            instance=budgets,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BudgetSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(['get', 'patch', 'delete'])
def budget_api_detail(request, pk):
    budget = get_object_or_404(
        Budget.objects.get_published(),
        pk=pk
    )
    if request.method == 'GET':
        serializer = BudgetSerializer(
            instance=budget,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = BudgetSerializer(
            instance=budget,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )
    elif request.method == 'DELETE':
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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