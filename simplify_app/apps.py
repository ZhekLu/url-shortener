from django.apps import AppConfig
# from django.dispatch import Signal
#
# from simplify_app.utilities import send_activation_notification

# user_registered = Signal()


# def user_registered_dispatcher(sender, **kwargs):
#     send_activation_notification(kwargs['instance'], kwargs['domain'])
#
#
# user_registered.connect(user_registered_dispatcher)


class SimplifyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simplify_app'
