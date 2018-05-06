from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View, UpdateView
# Create your views here.

from .models import Topic
from .forms import TopicCreateForm
from modal.views import AjaxCreateView
User = get_user_model()


class TopicFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        topic_to_toggle = request.POST.get("model_name")
        topic_, is_following = Topic.objects.toggle_follow_toggle(request.user, topic_to_toggle)
        return redirect(f"/topic/{request.user.username}/")


class TopicViewToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        topic_to_toggle = request.POST.get("model_name")
        topic_, is_following = Topic.objects.toggle_view_topic(request.user, topic_to_toggle)
        return redirect(f"/question/{request.user.username}/")


class TopicCreateView(LoginRequiredMixin, CreateView):
    form_class = TopicCreateForm
    template_name = 'topics/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TopicCreateView, self).get_context_data(*args, **kwargs)
        is_following_topic = []
        for top in Topic.objects.all():
            if top in self.request.user.is_following_topic.all():
                is_following_topic.append(top)
        context['is_following_topic'] = is_following_topic
        query = self.request.GET.get('q')
        qs = Topic.objects.search(query)
        if qs.exists():
            context['topics'] = qs
        return context


class TopicAjaxCreateView(AjaxCreateView):
    form_class = TopicCreateForm
    template_name = 'forms/create_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TopicAjaxCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create Topic'
        context['header'] = 'using name of an existing topic will be rejected'
        context['button_name'] = 'Add'
        return context
