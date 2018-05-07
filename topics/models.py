from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL


class TopicQuerySet(models.query.QuerySet):
    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)
            ).distinct()
        return self


class TopicManager(models.Manager):
    def toggle_follow_toggle(self, request_user, topic_to_toggle):
        topic_ = Topic.objects.get(name__iexact=topic_to_toggle)
        user = request_user
        is_following = False
        if user in topic_.followers.all():
            topic_.followers.remove(user)
        else:
            topic_.followers.add(user)
            is_following = True
        return topic_, is_following

    def toggle_view_topic(self, request_user, topic_to_toggle):
        topic_ = Topic.objects.get(name__iexact=topic_to_toggle)
        user = request_user
        is_following = False
        if user in topic_.viewers.all():
            topic_.viewers.remove(user)
        else:
            topic_.viewers.add(user)
            is_following = True
        return topic_, is_following

    def get_queryset(self):
        return TopicQuerySet(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


class Topic(models.Model):
    name = models.CharField(max_length=120)
    followers = models.ManyToManyField(User, related_name='is_following_topic', blank=True)  # user.is_following.all()
    viewers = models.ManyToManyField(User, related_name='is_viewing_topic', blank=True)
    # following         = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TopicManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # get_absolute_url
        # return f"/restaurants/{self.slug}"
        return reverse('topics:create')
