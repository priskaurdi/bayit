from collections import defaultdict

from attr import attr
from rest_framework import serializers

from authors.validators import AuthorBudgetValidator
from tag.models import Tag

from .models import Budget


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit',
            'preparation_steps', 'scheduled_date', 'scheduled_time',  # ainda precisa no modelo
            'schedule_data',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    schedule_data = serializers.DictField(
        write_only=True, 
        required=False
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True, source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='budgets:budgets_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, obj):
        return f'{obj.preparation_time} {obj.preparation_time_unit}'
    
    def get_schedule_data(self, obj):
        return {
            "date": obj.scheduled_date,
            "time": obj.scheduled_time
        }

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)

        AuthorBudgetValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )

        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule_data', None)
        if schedule_data:
            validated_data['scheduled_date'] = schedule_data.get('date')
            validated_data['scheduled_time'] = schedule_data.get('time')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        schedule_data = validated_data.pop('schedule_data', None)
        if schedule_data:
            validated_data['scheduled_date'] = schedule_data.get('date')
            validated_data['scheduled_time'] = schedule_data.get('time')
        return super().update(instance, validated_data)