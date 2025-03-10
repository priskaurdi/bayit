from django.contrib import admin

from .models import Budget, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
