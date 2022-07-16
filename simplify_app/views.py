from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.signing import BadSignature
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.views.generic import UpdateView, CreateView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from simplify_app.forms import ChangeUserInfoForm, UserPasswordChangeForm, LoginForm, SimpleUrlForm, RegisterUserForm
from simplify_app.models import SimpleUrl, User
from simplify_app.utilities import create_simple_url, signer


# App

def index(request):
    result_link = None
    if request.method == 'POST':
        form = SimpleUrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            simple_url_id = create_simple_url(original_url, request.user)
            result_link = 'http://' + get_current_site(request).name + '/' + simple_url_id

    else:
        form = SimpleUrlForm()
    context = {'form': form, 'result_link': result_link}
    return render(request, 'simplify_app/home/index.html', context)


def result(request, pk):
    try:
        url = get_object_or_404(SimpleUrl, simple_url_id=pk)
    except Http404:
        return render(request, 'simplify_app/home/invalid_url.html')
    return redirect(url.original_url)


# Profile

@login_required
def profile(request):
    context = {'urls': SimpleUrl.objects.filter(user=request.user.pk),
               'link_start': 'http://' + get_current_site(request).name + '/'}
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
    template_name = 'simplify_app/authentication/logout.html'


# Register

class RegisterUserView(CreateView):
    model = User
    template_name = 'simplify_app/authentication/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('simplify_app:register_done')

    def get_form_kwargs(self):
        kwargs = super(RegisterUserView, self).get_form_kwargs()
        current_site = get_current_site(self.request)
        kwargs.update({'domain': current_site.domain})
        return kwargs


class RegisterDoneView(TemplateView):
    template_name = 'simplify_app/authentication/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'simplify_app/authentication/bad_signature.html')

    user = get_object_or_404(User, username=username)
    if user.is_activated:
        template = 'simplify_app/authentication/user_is_activated.html'
    else:
        template = 'simplify_app/authentication/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)
