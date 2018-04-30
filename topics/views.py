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
        topic_to_toggle = request.POST.get("topic")
        topic_, is_following = Topic.objects.toggle_follow(request.user, topic_to_toggle)
        return redirect(f"/topic/{request.user.username}/")


class TopicViewToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        topic_to_toggle = request.POST.get("topic")
        topic_, is_following = Topic.objects.toggle_view(request.user, topic_to_toggle)
        return redirect(f"/question/{request.user.username}/")


# class TopicDetailView(DetailView):
#     template_name = 'topics/user.html'

#     def get_object(self):
#         return self.kwargs.get("topic")

#     def get_context_data(self, *args, **kwargs):
#         context = super(TopicDetailView, self).get_context_data(*args, **kwargs)
#         is_followingContext = []
#         for top in Topic.objects.all():
#             if top in self.request.user.is_followingT.all():
#                 is_followingContext.append(top)
#         context['is_followingContext'] = is_followingContext
#         query = self.request.GET.get('q')
#         qs = Topic.objects.search(query)
#         if qs.exists():
#             context['topics'] = qs
#         return context


class TopicCreateView(LoginRequiredMixin, UpdateView):
    form_class = TopicCreateForm
    template_name = 'topics/user.html'

    def get_object(self):
        return self.kwargs.get("topic")

    def form_valid(self, form):  # i think cbv calls this by default test later to remove
        instance = form.save(commit=False)
        return super(TopicCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TopicCreateView, self).get_context_data(*args, **kwargs)
        is_followingContext = []
        for top in Topic.objects.all():
            if top in self.request.user.is_followingT.all():
                is_followingContext.append(top)
        context['is_followingContext'] = is_followingContext
        query = self.request.GET.get('q')
        qs = Topic.objects.search(query)
        if qs.exists():
            context['topics'] = qs
        return context


class TopicAjaxCreateView(AjaxCreateView):
    form_class = TopicCreateForm
    template_name = 'topics/snippet/create_form.html'
