from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from topics.models import Topic
from profiles.models import Profile
from questions.models import Question

User = settings.AUTH_USER_MODEL


class AnswerQuerySet(models.query.QuerySet):
    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)
            ).distinct()
        return self


class AnswerManager(models.Manager):
    def toggle_follow_answer(self, request_user, Answer_to_toggle):
        Answer_ = Answer.objects.get(name__iexact=Answer_to_toggle)
        user = request_user
        is_following = False
        if user in Answer_.followers.all():
            Answer_.followers.remove(user)
        else:
            Answer_.followers.add(user)
            is_following = True
        return Answer_, is_following

    def toggle_follow_reply_answer(self, request_user, Answer_to_toggle):
        Answer_ = Answer.objects.get(name__iexact=Answer_to_toggle)
        user = request_user
        Answers = Answer.objects.filter(commentors=user)
        for ans in Answers:
            ans.commentors.remove(user)
        Answer_.commentors.add(user)
        is_following = True
        return Answer_, is_following

    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


class Answer(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)  # class_instance.model_set.all() # Django Models Unleashed JOINCFE.com
    followers = models.ManyToManyField(User, related_name='is_following_answer', blank=True)  # user.is_following.all()
    # following         = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    commentors = models.ManyToManyField(User, related_name='is_replying_answer', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # get_absolute_url
        ques = Question.objects.get(answer=self)
        return reverse('feedback:create', kwargs={'slug': ques.slug})

    @property
    def title(self):
        return self.name


class CommentManager(models.Manager):
    def toggle_follow_comment(self, request_user, Comment_to_toggle):
        Comment_ = Comment.objects.get(name__iexact=Comment_to_toggle)
        user = request_user
        is_following = False
        if user in Comment_.followers.all():
            Comment_.followers.remove(user)
        else:
            Comment_.followers.add(user)
            is_following = True
        return Comment_, is_following


class Comment(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(Profile)
    answer = models.ForeignKey(Answer)  # class_instance.model_set.all() # Django Models Unleashed JOINCFE.com
    followers = models.ManyToManyField(User, related_name='is_following_comment', blank=True)
    # user.is_following.all()
    # following         = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # get_absolute_url
        ans = Answer.objects.get(comment=self)
        ques = Question.objects.get(answer=ans)
        return reverse('feedback:create', kwargs={'slug': ques.slug})

    @property
    def title(self):
        return self.name
