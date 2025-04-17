from django.apps import AppConfig


class BudgetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgets'

    def ready(self, *args, **kwargs) -> None:
        import budgets.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready