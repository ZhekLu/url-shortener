from django.urls import path

from simplify_app.views import index, UserPasswordChangeView, ChangeUserInfoView, profile, UserLogoutView, UserLoginView

app_name = 'simplify_app'

urlpatterns = [
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('', index, name='index'),
]
