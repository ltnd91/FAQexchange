from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
# Create your views here.

from .models import Question
from profiles.models import Profile
from topics.models import Topic
from .forms import QuestionCreateForm, QuestionFilterForm
from modal.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
User = get_user_model()


class QuestionFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_to_toggle = request.POST.get("question")
        question_, is_following = Question.objects.toggle_follow(request.user, question_to_toggle)
        return redirect(f"/question/{request.user.username}/")


class QuestionFollowToggle2(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_to_toggle = request.POST.get("question")
        question_, is_following = Question.objects.toggle_follow(request.user, question_to_toggle)
        return redirect(f"/feedback/{question_.slug}/")


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = 'questions/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(*args, **kwargs)
        is_followingContext = []
        for ques in Question.objects.all():
            if ques in self.request.user.is_followingQ.all():
                is_followingContext.append(ques)
        context['is_followingContext'] = is_followingContext
        query = self.request.GET.get('q')
        qs = Question.objects.search(query)
        context['profiles'] = Profile.objects.filter(followers=self.request.user)
        context['topics'] = Topic.objects.filter(followers=self.request.user)
        if qs.exists():
            context['questions'] = qs
        return context


class QuestionAjaxCreateView(AjaxCreateView):
    form_class = QuestionCreateForm
    template_name = 'questions/snippet/create_form.html'

    def form_valid(self, form):  # i think cbv calls this by default test later to remove
        instance = form.save(commit=False)
        instance.owner = Profile.objects.get(user=self.request.user)
        return super(QuestionAjaxCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(QuestionAjaxCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create questions'
        return context


class QuestionAjaxUpdateView(AjaxUpdateView):
    form_class = QuestionFilterForm
    template_name = 'questions/snippet/filter_form.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Filter questions'
        return context


class QuestionAjaxUpdateView2(AjaxUpdateView):
    form_class = QuestionCreateForm
    template_name = 'questions/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Question.objects.filter(owner=profile_)

    def get_form_kwargs(self):
        kwargs = super(QuestionAjaxUpdateView2, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxUpdateView2, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit questions'
        return context


class QuestionAjaxDeleteView(AjaxDeleteView):
    form_class = QuestionCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Question.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Question'
        return context
