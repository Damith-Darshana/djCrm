from typing import Any
import random
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views import generic # generic includes the CRUD operations 
from django.contrib.auth.mixins import LoginRequiredMixin # this will check is the person loged in or not
from .mixins import OrganizerAndLoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm ,AgentModelFormNew

class AgentListView(OrganizerAndLoginRequiredMixin,generic.ListView):
  template_name = "agents/agent-list.html"
  # queryset = Agent.objects.all() # we could use this. but let's use the following one for the query set 
  context_object_name = 'agentList'
  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)

class AgentCreateView(OrganizerAndLoginRequiredMixin,generic.CreateView):
  template_name="agents/agent-create.html"
  form_class = AgentModelFormNew
  def get_success_url(self):
    return reverse('agents:agent-list')
  
  #in the AgentModelForm we didn't add the organization field. we going to add it in here 

  def form_valid(self,form):

    # agent = form.save(commit=False)
    # agent.organization = self.request.user.userprofile
    # agent.save()
#the above ones were used when AgentModelForm is Used
#now we going to use AgentModelFormNew model so i will create the user first then the Agent as follows
      newUser = form.save(commit=False) # do not save the data intothe database yet
      newUser.is_agent = True           # make that newly created user as and Agent
      newUser.is_organizer = False 
      newUser.set_password(f"{random.randint(0,1000000)}")     # now he is not an Organizer
      newUser.save()                    # this will save the User account, now create the Agent 

      Agent.objects.create(
        user=newUser,
        organization = self.request.user.userprofile
      )
      send_mail(
        subject="You are Invited to Become as an Agent",
        message="You are Requested to become a member of DJCRM and become one of our Agent",
        from_email="admin@gmail.com",
        recipient_list = [newUser.email]
      )
      return super(AgentCreateView,self).form_valid(form)
    
class AgentDetailView(OrganizerAndLoginRequiredMixin,generic.DetailView):
  template_name="agents/agent-detail.html"
  context_object_name = "agent"
  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)


class AgentUpdateView(OrganizerAndLoginRequiredMixin,generic.UpdateView):
  template_name="agents/agent-update.html"
  form_class = AgentModelForm
  context_object_name ="agentUpdate"

  def get_queryset(self):
    return  Agent.objects.all()

  def get_success_url(self) :
    agent_pk = self.object.pk  # Access the updated object's primary key
    return reverse('agents:agent-detail', kwargs={'pk': agent_pk})
  
class AgentDeleteView(OrganizerAndLoginRequiredMixin,generic.DeleteView):
  template_name="agents/agent-delete.html"
  form_class=AgentModelForm
  context_object_name = 'agentDelete'

  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)
  
  def get_success_url(self):
    return reverse('agents:agent-list')