from django import forms
from . import models

class PostForm(forms.ModelForm):

    body = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
        'rows':'3',
        'placeholder':'Share something with the world!'
        })
    )

    image = forms.ImageField(required=False)

    class Meta():
        model = models.Post
        fields = ('body', 'image')

class CommentForm(forms.ModelForm):

    comment = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
        'rows':'1',
        'placeholder':'Comment...'
        })
    )
    class Meta():
        model = models.Comment
        fields = ('comment',)


class ProfileForm(forms.ModelForm):

    class Meta():
        model = models.UserProfile

        fields = ('name', 'bio', 'gender', 'birth_date', 'location', 'profile_pic', 'profile_background')


class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'Quote'
        })
    )

class exploreForm(forms.Form):
    query = forms.CharField(
        label='',
        widget = forms.TextInput(attrs={
            'placeholder':'search anything you want...',
        })
    )