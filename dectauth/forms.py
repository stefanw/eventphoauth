import re

from django import forms


NUM_ONLY = re.compile('\d{4,}')


class StartChallengeForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label='Your DECT extension',
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if NUM_ONLY.match(username) is None:
            raise forms.ValidationError('Please provide a valid DECT extension')
        return username
