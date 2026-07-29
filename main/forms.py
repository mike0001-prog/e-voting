from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate
class VoteForm(forms.Form):
    candidate = forms.IntegerField(required=True)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField( label="Matric No",max_length=150,required=True,help_text="Matric No. should be in this format lascoco_nd_com_26_001")
    # email = forms.EmailField(required=True)
    last_name = forms.CharField(max_length=150,required=True)
    first_name = forms.CharField(max_length=150,required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field_name,field in self.fields.items():
        #     print(field.error_messages)
     


class CandidateCreationForm(forms.ModelForm):
    # name_of_candidate = forms.CharField()

    class Meta:
        model = Candidate
        fields =  ["position","candidate_photo"]