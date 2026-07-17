from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate
class VoteForm(forms.Form):
    candidate = forms.IntegerField(required=True)

class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(max_length=150,required=True)
    first_name = forms.CharField(max_length=150,required=True)

class CandidateCreationForm(forms.ModelForm):
    # name_of_candidate = forms.CharField()

    class Meta:
        model = Candidate
        fields =  ["position","candidate_photo"]