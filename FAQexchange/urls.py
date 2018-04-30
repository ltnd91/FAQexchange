from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView, LogoutView

from profiles.views import ProfileFollowToggle, ProfileViewToggle, ProfileViewToggle2
from topics.views import TopicFollowToggle, TopicViewToggle, TopicAjaxCreateView
from questions.views import QuestionFollowToggle, QuestionFollowToggle2, QuestionAjaxCreateView, QuestionAjaxUpdateView, QuestionAjaxUpdateView2, QuestionAjaxDeleteView
from feedback.views import AnswerAjaxCreateView, AnswerFollowToggle, AnswerAjaxUpdateView, AnswerAjaxDeleteView, CommentAjaxCreateView, CommentFollowToggle, CommentAjaxUpdateView, CommentAjaxDeleteView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^profile-view/$', ProfileViewToggle.as_view(), name='view'),
    url(r'^profile-view2/$', ProfileViewToggle2.as_view(), name='view2'),
    url(r'^topic-follow/$', TopicFollowToggle.as_view(), name='followT'),
    url(r'^topic-view/$', TopicViewToggle.as_view(), name='viewT'),
    url(r'^topic-create/$', TopicAjaxCreateView.as_view(), name='topicCreate'),
    url(r'^question-follow/$', QuestionFollowToggle.as_view(), name='followQ'),
    url(r'^question-follow2/$', QuestionFollowToggle2.as_view(), name='followQ2'),
    url(r'^question-create/$', QuestionAjaxCreateView.as_view(), name='questionCreate'),
    url(r'^question-update/(?P<pk>\d+)/$', QuestionAjaxUpdateView.as_view(), name='questionUpdate'),
    url(r'^(?P<pk>[\w-]+)/question-edit/$', QuestionAjaxUpdateView2.as_view(), name='questionEdit'),
    url(r'^(?P<pk>[\w-]+)/question-delete/$', QuestionAjaxDeleteView.as_view(), name='questionDelete'),
    url(r'^(?P<slug>[\w-]+)/answer-create/$', AnswerAjaxCreateView.as_view(), name='answerCreate'),
    url(r'^(?P<pk>[\w-]+)/answer-edit/$', AnswerAjaxUpdateView.as_view(), name='answerEdit'),
    url(r'^(?P<pk>[\w-]+)/answer-delete/$', AnswerAjaxDeleteView.as_view(), name='answerDelete'),
    url(r'^answer-follow/$', AnswerFollowToggle.as_view(), name='followA'),
    url(r'^(?P<pk>[\w-]+)/comment-create/$', CommentAjaxCreateView.as_view(), name='commentCreate'),
    url(r'^(?P<pk>[\w-]+)/comment-edit/$', CommentAjaxUpdateView.as_view(), name='commentEdit'),
    url(r'^(?P<pk>[\w-]+)/comment-delete/$', CommentAjaxDeleteView.as_view(), name='commentDelete'),
    url(r'^comment-follow/$', CommentFollowToggle.as_view(), name='followC'),
    url(r'^user/', include('profiles.urls', namespace='profiles')),
    url(r'^topic/', include('topics.urls', namespace='topics')),
    url(r'^question/', include('questions.urls', namespace='questions')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
]
