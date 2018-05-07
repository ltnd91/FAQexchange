from django import forms

from topics.models import Topic

from .models import Answer, Comment
from profiles.models import Profile
from questions.models import Question


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'name',
            'question',
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Answer.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Name already exist")
        return name

    def __init__(self, slug=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(kwargs)
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = Question.objects.filter(slug=slug)  # .exclude(item__isnull=False)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'answer',
        ]

    def __init__(self, pk=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(kwargs)
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = Answer.objects.filter(pk=pk)  # .exclude(item__isnull=False)
