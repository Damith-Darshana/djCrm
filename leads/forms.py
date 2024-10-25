from django import forms
from .models import Lead,Agent

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Field,Layout

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
      'description',
      'phone_number',
      'email',
    )
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.helper = FormHelper()
    # Apply class to all labels
    self.fields['first_name'].widget.attrs.update({
      'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm border-l-4 border-l-purple-600',
      'placeholder': 'First Name',
      'id':'firstName',
    
    })
  
    self.fields['last_name'].widget.attrs.update({
      'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm border-l-4 border-l-purple-600',
      'placeholder': 'Last Name',
    })
    
    self.fields['age'].widget.attrs.update({
      'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm border-l-4 border-l-purple-600',
      'placeholder': 'Last Name',
    })
    self.fields['agent'].widget.attrs.update({
      'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-900 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm border-l-4 border-l-purple-600',
      
    })

    self.helper.label_class = "block text-sm font-medium text-purple-500"
     # Apply class to all labels
   
   


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



class LeadCategoryUpdateForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields = (
      'category',
    )

