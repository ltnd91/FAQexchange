from django import forms

from .models import Profile


class ProfileFilterForm(forms.ModelForm):
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
        super(ProfileFilterForm, self).__init__(*args, **kwargs)
