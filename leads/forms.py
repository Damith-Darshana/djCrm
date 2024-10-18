from django import forms
from .models import Lead,Agent

from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields=("username",)
    field_classes={'username':UsernameField}


class LeadModelForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields=(
      'first_name',
      'last_name',
      'age',
      'agent',
    )

class LeadForm(forms.Form):
  first_name = forms.CharField()
  last_name  = forms.CharField()
  age = forms.IntegerField(min_value=0)


# this form is used to select an agent for a lead who haven't been assigned an agent
class AssignAgentForm(forms.Form):
  agent = forms.ModelChoiceField(     # the field is a option field where all the agents belong to the lead organization will be appeared 
    queryset=Agent.objects.none()     # for now keep it as it is untill we assign the correct queryset from below
  )
 
  def __init__(self, *args, **kwargs):  
      
      request = kwargs.pop("request")   # get the request user. which is the added kwargs within the view 
      agents = Agent.objects.filter(organization = request.user.userprofile)  # here we get those agents belongs to the same organization that the lead belongs 
      super(AssignAgentForm, self).__init__(*args, **kwargs) 
      self.fields["agent"].queryset = agents  # assign the query set here and now it will be this instead of none as above 