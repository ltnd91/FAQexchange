
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
# Create your views here.

from .models import Profile
User = get_user_model()


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/user/{request.user.username}/")


class ProfileViewToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_view(request.user, username_to_toggle)
        return redirect(f"/question/{request.user.username}/")


class ProfileViewToggle2(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_view(request.user, username_to_toggle)
        return redirect(f"/feedback/")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_followingContext = []
        for pro in Profile.objects.all():
            if pro in self.request.user.is_following.all():
                is_followingContext.append(pro)
        context['is_followingContext'] = is_followingContext
        query = self.request.GET.get('q')
        qs = Profile.objects.search(query)
        if qs.exists():
            context['profiles'] = qs
        return context
