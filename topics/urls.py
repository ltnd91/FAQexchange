from django.conf.urls import url

from .views import TopicCreateView  # TopicDetailView  #

urlpatterns = [
    # url(r'^(?P<username>[\w-]+)/$', TopicDetailView.as_view(), name='detail'),
    url(r'^$', TopicCreateView.as_view(), name='create'),
]
#
