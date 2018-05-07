
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
from modal.views import AjaxUpdateView
# Create your views here.

from .models import Profile
from questions.models import Question
from .forms import ProfileFilterForm, RegisterForm
User = get_user_model()


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login")
    return redirect("/login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/login/'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("model_name")
        profile_, is_following = Profile.objects.toggle_follow_profile(request.user, username_to_toggle)
        return redirect(f"/user/")


class ProfileViewToggleQuestion(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("model_name")
        profile_, is_following = Profile.objects.toggle_view_profile(request.user, username_to_toggle)
        return redirect(f"/question/")


class ProfileViewToggleFeedback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("model_name")
        profile_, is_following = Profile.objects.toggle_view_profile(request.user, username_to_toggle)
        question_ = Question.objects.get(viewers=request.user)
        return redirect(f"/feedback/{question_.slug}/")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.request.user.username
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        is_following_profile = []
        for pro in Profile.objects.all():
            if pro in self.request.user.is_following_profile.all():
                is_following_profile.append(pro)
        context['is_following_profile'] = is_following_profile
        query = self.request.GET.get('q')
        qs = Profile.objects.search(query)
        if qs.exists():
            context['profiles'] = qs
        return context


class ProfileAjaxUpdateView(AjaxUpdateView):
    form_class = ProfileFilterForm
    template_name = 'forms/create_form.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileAjaxUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Filter'
        context['button_name'] = 'Update'
        return context
