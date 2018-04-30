from django import forms

from topics.models import Topic

from .models import Question
from profiles.models import Profile


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'name',
            'topic',
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Question.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Question already exist")
        return name

    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        # print(user)
        print(kwargs)
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(followers=user)


class QuestionFilterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'showAllTopics',
            'showAllUsers',
        ]

    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(user)
        print(kwargs)
        super(QuestionFilterForm, self).__init__(*args, **kwargs)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("We do not accept edu emails")
    #     return email
