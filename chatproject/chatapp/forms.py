from django.forms import ModelForm
from django import forms
from .models import Chat


from django.contrib.auth.models import User

class ChatForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Chat
        fields = ['name', 'participants', 'admin']


class ParticipantForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)