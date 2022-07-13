from django.urls import path

from simplify_app.views import index

app_name = 'simplify_app'

urlpatterns = [
    path('', index, name='index'),
]
