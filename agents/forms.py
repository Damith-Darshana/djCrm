from django import forms
from leads.models import Agent
from django.contrib.auth import get_user_model #  Return the User model that is active in this project.

User = get_user_model() # we save it 

#this model is used to create the Agent.but the problem is he should be a user before 
class AgentModelForm(forms.ModelForm):
  class Meta:
    model =Agent
    fields=(
      'user', # we don't specify the organization field here 
    )

#in this updated form version. we create user account and agent account at the same time
class AgentModelFormNew(forms.ModelForm):
  class Meta:
    model = User # now the model is User and we create Agent witin the Views.py file before commit changes to the database
    fields=(   #define the fields
      'username',
      'first_name',
      'last_name',
      'email',
    )
