from django.conf.urls import url

from .views import AnswerCreateView  # ,TopicDetailView

urlpatterns = [
    #url(r'^(?P<username>[\w-]+)/$', TopicDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', AnswerCreateView.as_view(), name='create'),
]
