from typing import Any
from django.db.models.query import QuerySet     # Import to handle database Query Sets            
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.views import generic               # This includes all the CRUD Operations 
from .models import Lead,Category #This is the Lead Model or Table we created in Models.py we use this here to interact with the tabel data
from .forms import LeadModelForm, CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm  #this includes the Custom Forms or Overridden forms crated within the Forms.py file

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin # This Method will check if the Requesting User is Logged in or Not
from agents.mixins import OrganizerAndLoginRequiredMixin  # This is the My custom created LoginRequired Mixin created within the Agents App 
# Create your views here.

@login_required
def user_logout(request):
   """Logs out the user and renders the logged_out template."""
   logout(request)
   return render(request,"registration/logged_out.html")











"""
**SignUpView**

This view handles user registration using the custom `CustomUserCreationForm`.
"""

class SignUpView(generic.CreateView):
  template_name ="registration/signup.html"  #this is the Template this class going to Use 
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('login')


"""
**LandingPageView**

This view simply renders the `landing-page.html` template.
"""
class LandingPageView(generic.TemplateView):
  template_name = "landing-page.html"
  context_object_name = 'leads'

  def get_queryset(self):
    queryset = Lead.objects.all()
    return queryset
  

"""
**LeadListView**

This view displays a list of leads for the currently logged-in user,
filtering based on their role (organizer or agent).

- LoginRequiredMixin ensures only authenticated users can access this view.
"""


class LeadListView(LoginRequiredMixin,generic.ListView):
  template_name = "leads/leads-list.html"
  context_object_name = "leads"

  def get_queryset(self):
    user = self.request.user  #Assign the Current user
    if user.is_organizer:     # Check if the user is an Organizer True
      queryset = Lead.objects.filter(
        # get all the leads where there organization equal to the organization of the current User and agent field is not null 
        organization = user.userprofile, 
        agent__isnull =False  # this will get leads who are assigned to an Agent
    
      )
    else: # else meaning now  the current user is an Agent 
      queryset = Lead.objects.filter(
        #
        organization = user.agent.organization,
        agent__isnull =False
      )
      queryset = queryset.filter(
        # an agent is also a user
        # so this query will get leads who have assigned to him
        agent__user = user # this is like saying get every leads who have assigned to this agent 
      )
    return queryset
  

  # The following is the way to classify the leads with agents and with no-agents 
  # The method is used to overide the context and add aditional things to the context  
  def get_context_data(self, **kwargs):
    context = super(LeadListView, self).get_context_data(**kwargs)
    user = self.request.user
    if user.is_organizer:
      queryset = Lead.objects.filter(
        organization = user.userprofile, 
        agent__isnull = True
      )
      context.update({
        "unassigned_leads" : queryset
      })
    return context
  




class LeadDetailView(LoginRequiredMixin,generic.DetailView):
  template_name = "leads/lead-detail.html"
  context_object_name ="lead"

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer:
      queryset = Lead.objects.filter(organization = user.userprofile)
    else:
      queryset = Lead.objects.filter(
        organization = user.agent.organization, #give the leads who are in the same organization as the agent
        agent__user = user
      )
    return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin,generic.CreateView):

  template_name="leads/lead-create.html"
  form_class = LeadModelForm

  def get_success_url(self):
    return reverse('leads:lead-list')
  
  def form_valid(self,form):
    lead = form.save(commit=False)
    lead.organization = self.request.user.userprofile
    lead.save()

    return super(LeadCreateView,self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin,generic.UpdateView):
  template_name="leads/lead-update.html"
  form_class = LeadModelForm
  
  def get_queryset(self):
    queryset = Lead.objects.filter(organization = self.request.user.userprofile)
    return queryset

  def get_success_url(self):
    return reverse("leads:lead-list")
  
class LeadDeleteView(OrganizerAndLoginRequiredMixin,generic.DeleteView):
  template_name = "leads/lead-delete.html"
 
  def get_success_url(self):
    return reverse("leads:lead-list")
  
  def get_queryset(self):
    queryset = Lead.objects.filter(organization = self.request.user.userprofile)
    return queryset

#This class View is used to assign an agent for leads who are in the Unassigned Agents part
class AssignAgentView(OrganizerAndLoginRequiredMixin,generic.FormView):
  template_name = "leads/assign-agent.html"
  form_class = AssignAgentForm

  #use this method to add additional kwags by using the update func
  def get_form_kwargs(self,**kwags) -> dict[str, Any]:
    kwags =  super(AssignAgentView,self).get_form_kwargs(**kwags)
    kwags.update({
      "request":self.request
    })
    return kwags

  def form_valid(self, form):
    agent = form.cleaned_data["agent"] # get the agent that the user selected in the form
    lead = Lead.objects.get(id = self.kwargs["pk"])  # take the lead object by using the primary key within the url
    lead.agent = agent   # assign the agent to the grabbed lead 
    lead.save()  # save data 
    return super().form_valid(form) 

  def get_success_url(self):
    return reverse('leads:lead-list')
  
class CategoryView(LoginRequiredMixin,generic.ListView):
  template_name = 'leads/category-view.html'
  context_object_name = 'categoryList'

  def get_context_data(self, **kwargs):
    context = super(CategoryView,self).get_context_data(**kwargs)
    user = self.request.user
    if user.is_organizer :
      queryset = Lead.objects.filter(
        organization = user.userprofile
      )
    else:
      queryset = Lead.objects.filter(
        organization = user.agent.organization
      )
    
    unAssignedLeadCount=queryset.filter(category__isnull = True).count()

    context.update({
        "unAssignedLeadCount":unAssignedLeadCount
      
    })
    return context
    

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer :
      queryset = Category.objects.filter(
        organization = user.userprofile
      )
    else:
      queryset = Category.objects.filter(
        organization = user.agent.userprofile
      )
    return queryset
  

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
  template_name = "leads/category-detail-view.html"
  context_object_name ='category'


  def get_context_data(self, **kwargs):
    context = super(CategoryDetailView,self).get_context_data(**kwargs)
    # qs = Lead.objects.filter(category = self.get_object())  we use the following line instead of this because it do the same thing 
    leads = self.get_object().leads.all()
    

    context.update({
        "leads":leads
      
    })
    return context


  
  def get_queryset(self):
    user = self.request.user
    if user.is_organizer :
      queryset = Category.objects.filter(
        organization = user.userprofile
      )
    else:
      queryset = Category.objects.filter(
        organization = user.agent.userprofile
      )
    return queryset
  
class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
  template_name = 'leads/category-update-view.html'
  form_class = LeadCategoryUpdateForm

  def get_queryset(self):
    user = self.request.user
    if user.is_organizer :
      queryset = Lead.objects.filter(
        organization = user.userprofile
      )
    else:
      queryset = Lead.objects.filter(
        organization = user.agent.userprofile
      )
    return queryset
  
  def get_success_url(self) -> str:
    return reverse('leads:lead-detail',kwargs={"pk":self.get_object().id})








