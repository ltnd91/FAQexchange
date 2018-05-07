from django import forms

from .models import Topic


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'name',
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Topic.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Topic already exist")
        return name

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("We do not accept edu emails")
    #     return email
