from unicodedata import category

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Budget
from ..serializers import BudgetSerializer, TagSerializer


class BudgetAPIv2Pagination(PageNumberPagination):
    page_size = 2
    
class BudgetAPIv2ViewSet(ModelViewSet):
    queryset = Budget.objects.get_published()
    serializer_class = BudgetSerializer
    pagination_class = BudgetAPIv2Pagination
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example"] = 'this is in context now'
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    
    def partial_update(self, request, *args, **kwarg):
        pk = kwarg.get('pk')

        budget = self.get_queryset().filter(pk=pk).first()
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