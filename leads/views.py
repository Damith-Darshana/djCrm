from django.shortcuts import render, reverse, redirect
from django.views import generic
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SignUpView(generic.CreateView):
  template_name ="registration/signup.html"
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('login')




class LandingPageView(generic.TemplateView):
  template_name = "landing-page.html"

class LeadListView(LoginRequiredMixin,generic.ListView):
  template_name = "leads/leads-list.html"
  queryset = Lead.objects.all()
  context_object_name = "leads"

class LeadDetailView(LoginRequiredMixin,generic.DeleteView):
  template_name = "leads/lead-detail.html"
  queryset=Lead.objects.all()
  context_object_name ="lead"

class LeadCreateView(LoginRequiredMixin,generic.CreateView):

  template_name="leads/lead-create.html"
  form_class = LeadModelForm

  def get_success_url(self):
    return reverse('leads:lead-list')


class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
  template_name="leads/lead-update.html"
  form_class = LeadModelForm
  queryset = Lead.objects.all()

  def get_success_url(self):
    return reverse("leads:lead-detail",kwargs={"pk":self.object.pk})
  
class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
  template_name = "leads/lead-delete.html"
  queryset = Lead.objects.all()

  def get_success_url(self):
    return reverse("leads:lead-list")
