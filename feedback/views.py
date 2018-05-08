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
        Answer_to_toggle = request.POST.get("model_name")
        Answer_, is_following = Answer.objects.toggle_follow_answer(request.user, Answer_to_toggle)
        Question_ = Question.objects.get(answer=Answer_)
        return redirect(f"/feedback/{ Question_.slug }/")


class ReplyAnswerFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Answer_to_toggle = request.POST.get("model_name")
        Answer_, is_following = Answer.objects.toggle_follow_reply_answer(request.user, Answer_to_toggle)
        Question_ = Question.objects.get(answer=Answer_)
        return redirect(f"/feedback/{ Question_.slug }/")


class CommentFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Comment_to_toggle = request.POST.get("model_name")
        Comment_, is_following = Comment.objects.toggle_follow_comment(request.user, Comment_to_toggle)
        Answer_ = Answer.objects.get(comment=Comment_)
        Question_ = Question.objects.get(answer=Answer_)
        return redirect(f"/feedback/{ Question_.slug }/")


class AnswerCreateView(LoginRequiredMixin, CreateView):
    form_class = AnswerCreateForm
    template_name = 'feedback/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(*args, **kwargs)
        is_following_answer = []
        is_following_comment = []
        is_following_profile = []
        is_following_question = []
        context['question'] = Question.objects.get(slug=self.kwargs.get("slug"))
        if context['question'] in self.request.user.is_following_question.all():
            is_following_question.append(context['question'])
        context['is_following_question'] = is_following_question
        is_viewing_question = Question.objects.filter(viewers=self.request.user)
        for ques in is_viewing_question:
            ques.viewers.remove(self.request.user)
        context['question'].viewers.add(self.request.user)
        query = self.request.GET.get('q')
        qs = Answer.objects.search(query)
        if qs.exists():
            context['answers'] = qs.filter(question=context['question']).order_by('-followers', '-updated','name').distinct('followers','updated','name')
            for ans in context['answers']:
                if ans.owner not in is_following_profile:
                    is_following_profile.append(ans.owner)
            for ans in context['answers']:
                if ans in self.request.user.is_following_answer.all():
                    is_following_answer.append(ans)
                if ans in self.request.user.is_replying_answer.all():
                    context['is_replying_answer'] = ans
                    context['is_viewing_comment'] = Comment.objects.filter(answer=context['is_replying_answer']).order_by('-followers', '-updated','name').distinct('followers','updated','name')
                    for comm in context['is_viewing_comment']:
                        if comm.owner not in is_following_profile:
                            is_following_profile.append(comm.owner)
        context['is_following_profile'] = is_following_profile
        context['is_following_answer'] = is_following_answer
        for comm in Comment.objects.all():
            if comm in self.request.user.is_following_comment.all():
                is_following_comment.append(comm)
        context['is_following_comment'] = is_following_comment
        context['comment_owner'] = Comment.objects.filter(owner=self.request.user.profile)
        context['answer_owner'] = Answer.objects.filter(owner=self.request.user.profile)
        context['question_owner'] = Question.objects.filter(owner=self.request.user.profile)
        return context


class CommentAjaxCreateView(AjaxCreateView):
    form_class = CommentCreateForm
    template_name = 'forms/create_form.html'

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
        context['title'] = "Add Comment"
        context['button_name'] = 'Add'
        return context


class CommentAjaxUpdateView(AjaxUpdateView):
    form_class = CommentCreateForm
    template_name = 'forms/create_form.html'

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
        context['button_name'] = 'Update'
        return context


class CommentAjaxDeleteView(AjaxDeleteView):
    form_class = CommentCreateForm
    template_name = 'forms/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Comment.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(CommentAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Comment'
        context['button_name'] = 'Delete'
        return context


class AnswerAjaxCreateView(AjaxCreateView):
    form_class = AnswerCreateForm
    template_name = 'forms/create_form.html'

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
        context['title'] = 'Add Answer'
        context['header'] = 'using name of an existing answer will be rejected'
        context['button_name'] = 'Add'
        return context


class AnswerAjaxUpdateView(AjaxUpdateView):
    form_class = AnswerCreateForm
    template_name = 'forms/create_form.html'

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
        context['button_name'] = 'Update'
        return context


class AnswerAjaxDeleteView(AjaxDeleteView):
    form_class = AnswerCreateForm
    template_name = 'forms/create_form.html'

    def get_queryset(self):
        profile_ = Profile.objects.get(user=self.request.user)
        return Answer.objects.filter(owner=profile_)

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerAjaxDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete Answer'
        context['button_name'] = 'Delete'
        return context
