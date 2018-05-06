from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from topics.models import Topic
from profiles.models import Profile

from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class QuestionQuerySet(models.query.QuerySet):
    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)
            ).distinct()
        return self


class QuestionManager(models.Manager):
    def toggle_follow_question(self, request_user, question_to_toggle):
        question_ = Question.objects.get(name__iexact=question_to_toggle)
        user = request_user
        is_following = False
        if user in question_.followers.all():
            question_.followers.remove(user)
        else:
            question_.followers.add(user)
            is_following = True
        return question_, is_following

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


class Question(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(Profile)
    topic = models.ForeignKey(Topic)  # class_instance.model_set.all() # Django Models Unleashed JOINCFE.com
    followers = models.ManyToManyField(User, related_name='is_followingQ', blank=True)  # user.is_following.all()
    # following         = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    viewers = models.ManyToManyField(User, related_name='is_viewing_question', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    objects = QuestionManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('feedback:create', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.name


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=Question)
