from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import Vote
class VoteForm(forms.Form):
    candidate = forms.IntegerField(required=True)

