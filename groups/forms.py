from django import forms 

from . import models 

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'description', 'cover')

class UpdateGroupForm(forms.ModelForm):
    
    class Meta:
        model = models.Group
        fields = ('description', 'cover', 'moderators','admin', 'ban')
        labels = {
            'ban': 'Remove ban from members:'
        }      
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        grp = kwargs.pop('grp')
        qs = models.Group.objects.get(name=grp.name)
        super(UpdateGroupForm, self).__init__(*args, **kwargs)
        self.fields['admin'].queryset = qs.members
        self.fields['moderators'].queryset = qs.members
        self.fields['ban'].queryset = qs.ban
        



class createpostform(forms.ModelForm):

    content = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
        'rows':'3',
        'placeholder':'Share something!'
        })
    )

    image = forms.ImageField(required=False)

    class Meta():
        model = models.GroupPost
        fields = ('content', 'image')


