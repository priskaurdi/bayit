from django.contrib import admin

# Register your models here.
from authors.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...