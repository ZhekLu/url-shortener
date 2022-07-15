from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from simplify_app.forms import ChangeUserInfoForm, UserPasswordChangeForm, LoginForm
from simplify_app.models import SimpleUrl, User


def index(request):
    return render(request, 'simplify_app/home/index.html')


# Profile

@login_required
def profile(request):
    context = {'urls': SimpleUrl.objects.filter(user=request.user.pk)}
    return render(request, 'simplify_app/profile/profile.html', context)


class ChangeUserInfoView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'simplify_app/profile/profile_edit.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('simplify_app:profile')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'simplify_app/profile/profile_password_change.html'
    success_url = reverse_lazy('simplify_app:profile')


# Login

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'simplify_app/authentication/login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'simplify_app/home/index.html'
