from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
# Create your views here.

from .models import Question
from profiles.models import Profile
from topics.models import Topic
from .forms import QuestionCreateForm
from .utils import unique_slug_generator
from modal.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
User = get_user_model()


class QuestionFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_to_toggle = request.POST.get("model_name")
        question_, is_following = Question.objects.toggle_follow_question(request.user, question_to_toggle)
        return redirect(f"/question/")


class QuestionFollowToggleFeedback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_to_toggle = request.POST.get("model_name")
        question_, is_following = Question.objects.toggle_follow_question(request.user, question_to_toggle)
        return redirect(f"/feedback/{question_.slug}/")


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = 'questions/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(*args, **kwargs)
        is_following_question = []
        is_unique_question = []
        for ques in Question.objects.all():
            if ques in self.request.user.is_following_question.all():
                is_following_question.append(ques)
        context['is_following_question'] = is_following_question
        query = self.request.GET.get('q')
        duplicateArray = Question.objects.search(query).order_by('followers')
        for ques in duplicateArray:
            if ques not in is_unique_question:
                is_unique_question.append(ques)
        context['profiles'] = Profile.objects.filter(followers=self.request.user)
        context['topics'] = Topic.objects.filter(followers=self.request.user)
        context['questions'] = is_unique_question
        context['question_owner'] = Question.objects.filter(owner=self.request.user.profile)
        context['is_following_profile_question'] = Profile.objects.filter(followers=self.request.user)
        return context


class QuestionAjaxCreateView(AjaxCreateView):
    form_class = QuestionCreateForm
    template_name = 'forms/create_form.html'

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
        context['header'] = 'using name of an existing question will be rejected'
        context['button_name'] = 'Add'
        return context


class QuestionAjaxUpdateView(AjaxUpdateView):
    form_class = QuestionCreateForm
    template_name = 'forms/create_form.html'

    def form_valid(self, form):  # i think cbv calls this by default test later to remove
        instance = form.save(commit=False)
        instance.slug = unique_slug_generator(instance)
        return super(QuestionAjaxUpdateView, self).form_valid(form)

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Question.objects.filter(owner=profile_)

    def get_form_kwargs(self):
        kwargs = super(QuestionAjaxUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit Question'
        context['button_name'] = 'Update'
        return context


class QuestionAjaxDeleteView(AjaxDeleteView):
    form_class = QuestionCreateForm
    template_name = 'forms/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Question.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Question'
        context['button_name'] = 'Delete'
        return context
