from django.apps import AppConfig

class AadharAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aadhar_app"

    def ready(self):
        import aadhar_app.templatetags.custom_filters
