from django.conf.urls import url

from .views import TopicCreateView  # TopicDetailView  #

urlpatterns = [
    # url(r'^(?P<username>[\w-]+)/$', TopicDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w-]+)/$', TopicCreateView.as_view(), name='create'),
]
#
