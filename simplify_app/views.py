import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from simplify_app.forms import ChangeUserInfoForm, UserPasswordChangeForm, LoginForm, SimpleUrlForm
from simplify_app.models import SimpleUrl, User


# App

def index(request):
    result_link = None
    if request.method == 'POST':
        form = SimpleUrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            simple_url_id = str(uuid.uuid4())[:5]
            result_link = 'http://' + get_current_site(request).name + '/' + simple_url_id
            simple_url = SimpleUrl(original_url=original_url, simple_url_id=simple_url_id,
                                   user=request.user)
            simple_url.save()

    else:
        form = SimpleUrlForm()
    context = {'form': form, 'result_link': result_link}
    return render(request, 'simplify_app/home/index.html', context)


def result(request, pk):
    url = SimpleUrl.objects.get(simple_url_id=pk)
    return redirect(url.original_url)

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
