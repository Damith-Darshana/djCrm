from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views import generic # generic includes the CRUD operations 
from django.contrib.auth.mixins import LoginRequiredMixin # this will check is the person loged in or not
from leads.models import Agent
from .forms import AgentModelForm

class AgentListView(LoginRequiredMixin,generic.ListView):
  template_name = "agents/agent-list.html"
  # queryset = Agent.objects.all() # we could use this. but let's use the following one for the query set 
  context_object_name = 'agentList'
  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)

class AgentCreateView(LoginRequiredMixin,generic.CreateView):
  template_name="agents/agent-create.html"
  form_class = AgentModelForm

  def get_success_url(self):
    return reverse('agents:agent-list')
  
  #in the AgentModelForm we didn't add the organization field. we going to add it in here 

  def form_valid(self,form):

    agent = form.save(commit=False)
    agent.organization = self.request.user.userprofile
    agent.save()
    return super(AgentCreateView,self).form_valid(form)
    
class AgentDetailView(LoginRequiredMixin,generic.DetailView):
  template_name="agents/agent-detail.html"
  context_object_name = "agent"
  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)


class AgentUpdateView(LoginRequiredMixin,generic.UpdateView):
  template_name="agents/agent-update.html"
  form_class = AgentModelForm
  context_object_name ="agentUpdate"

  def get_queryset(self):
    return  Agent.objects.all()

  def get_success_url(self) :
    agent_pk = self.object.pk  # Access the updated object's primary key
    return reverse('agents:agent-detail', kwargs={'pk': agent_pk})
  
class AgentDeleteView(LoginRequiredMixin,generic.DeleteView):
  template_name="agents/agent-delete.html"
  form_class=AgentModelForm
  context_object_name = 'agentDelete'

  def get_queryset(self):
    organization = self.request.user.userprofile # we gets the userprofile of the requested user 
    return Agent.objects.filter(organization = organization)
  
  def get_success_url(self):
    return reverse('agents:agent-list')