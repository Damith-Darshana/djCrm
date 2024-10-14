from django import forms
from leads.models import Agent

class AgentModelForm(forms.ModelForm):
  class Meta:
    model =Agent
    fields=(
      'user', # we don't specify the organization field here 
    )
