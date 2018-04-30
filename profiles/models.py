from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL


class ProfileQuerySet(models.query.QuerySet):
    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(user__username__icontains=query)
            ).distinct()
        return self


class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

    def toggle_view(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.viewers.all():
            profile_.viewers.remove(user)
        else:
            profile_.viewers.add(user)
            is_following = True
        return profile_, is_following

    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


class Profile(models.Model):
    user = models.OneToOneField(User)  # user.profile
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    viewers = models.ManyToManyField(User, related_name='is_viewing', blank=True)
    # user.is_following.all()
    # following         = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    showAllTopics = models.BooleanField(default=False)
    showAllUsers = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):  # get_absolute_url
        # return f"/restaurants/{self.slug}"
        return reverse('questionUpdate', kwargs={'pk': self.pk})


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]  # user__username=
        default_user_profile.followers.add(instance)
        profile.followers.add(default_user_profile.user)


post_save.connect(post_save_user_receiver, sender=User)
