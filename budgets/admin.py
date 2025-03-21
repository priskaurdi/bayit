from django.contrib import admin

from .models import Budget, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_publish']
    list_display_link = ['title', 'created_at']

admin.site.register(Category, CategoryAdmin)
