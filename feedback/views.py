from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
from django.core.urlresolvers import reverse
# Create your views here.

from questions.models import Question
from profiles.models import Profile
from topics.models import Topic
from .models import Answer, Comment

from .forms import AnswerCreateForm, CommentCreateForm
from modal.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
User = get_user_model()


class AnswerFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Answer_to_toggle = request.POST.get("answer")
        Answer_, is_following = Answer.objects.toggle_follow(request.user, Answer_to_toggle)
        ques_ = Question.objects.get(answer=Answer_)
        return redirect(f"/feedback/{ ques_.slug }/")


class CommentFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Comment_to_toggle = request.POST.get("comment")
        Comment_, is_following = Comment.objects.toggle_follow(request.user, Comment_to_toggle)
        Answer_ = Answer.objects.get(comment=Comment_)
        ques_ = Question.objects.get(answer=Answer_)
        return redirect(f"/feedback/{ ques_.slug }/")


class AnswerCreateView(LoginRequiredMixin, CreateView):
    form_class = AnswerCreateForm
    template_name = 'feedback/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(*args, **kwargs)
        is_followingContext = []
        is_followingContextA = []
        is_followingContextC = []
        ques = Question.objects.get(slug=self.kwargs.get("slug"))
        context['question'] = ques
        if ques in self.request.user.is_followingQ.all():
            is_followingContext.append(ques)
        context['is_followingContext'] = is_followingContext
        query = self.request.GET.get('q')
        qs = Answer.objects.search(query)
        context['profiles'] = Profile.objects.filter(followers=self.request.user)
        context['answers'] = Answer.objects.filter(question=ques)
        context['comments'] = Comment.objects.all()
        for comm in context['comments']:
            if comm in self.request.user.is_followingC.all():
                    is_followingContextC.append(comm)
        context['is_followingContextC'] = is_followingContextC
        for ans in context['answers']:
            if ans in self.request.user.is_followingA.all():
                is_followingContextA.append(ans)
        context['is_followingContextA'] = is_followingContextA
        if qs.exists():
            context['Answers'] = qs
        return context

class CommentAjaxCreateView(AjaxCreateView):
    form_class = CommentCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = Profile.objects.get(user=self.request.user)
        return super(CommentAjaxCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CommentAjaxCreateView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get("pk")
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(CommentAjaxCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = Answer.objects.get(pk=self.kwargs.get("pk")).owner
        return context

class CommentAjaxUpdateView(AjaxUpdateView):
    form_class = CommentCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Comment.objects.filter(owner=profile_)

    def get_form_kwargs(self):
        kwargs = super(CommentAjaxUpdateView, self).get_form_kwargs()
        comm = Comment.objects.get(pk=self.kwargs.get("pk"))
        ans = Answer.objects.get(comment=comm)
        kwargs['pk'] = ans.pk
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(CommentAjaxUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit Comment'
        return context


class CommentAjaxDeleteView(AjaxDeleteView):
    form_class = CommentCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Comment.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(CommentAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Comment'
        return context

class AnswerAjaxCreateView(AjaxCreateView):
    form_class = AnswerCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = Profile.objects.get(user=self.request.user)
        return super(AnswerAjaxCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AnswerAjaxCreateView, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs.get("slug")
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerAjaxCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = Question.objects.get(slug=self.kwargs.get("slug")).owner
        return context


class AnswerAjaxUpdateView(AjaxUpdateView):
    form_class = AnswerCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Answer.objects.filter(owner=profile_)

    def get_form_kwargs(self):
        kwargs = super(AnswerAjaxUpdateView, self).get_form_kwargs()
        ans = Answer.objects.get(pk=self.kwargs.get("pk"))
        ques = Question.objects.get(answer=ans)
        kwargs['slug'] = ques.slug
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerAjaxUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit Answer'
        return context


class AnswerAjaxDeleteView(AjaxDeleteView):
    form_class = AnswerCreateForm
    template_name = 'feedback/snippet/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Answer.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Answer'
        return context
