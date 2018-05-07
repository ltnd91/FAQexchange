from django.conf.urls import url

from .views import QuestionCreateView  # ,TopicDetailView

urlpatterns = [
    #url(r'^(?P<username>[\w-]+)/$', TopicDetailView.as_view(), name='detail'),
    url(r'^$', QuestionCreateView.as_view(), name='create'),
]
