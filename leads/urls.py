from django.urls import path
from .views import (
  LandingPageView,
  LeadListView, 
  LeadDetailView,
  LeadCreateView,
  LeadUpdateView,
  LeadDeleteView,
  AssignAgentView,
  CategoryView,
  CategoryDetailView,
  LeadCategoryUpdateView,
)

app_name = "leads"

urlpatterns = [

  path('',LeadListView.as_view(),name='lead-list'),
  path('<int:pk>/',LeadDetailView.as_view(),name='lead-detail'),
  path('create/',LeadCreateView.as_view(),name='lead-create'),
  path('<int:pk>/update/',LeadUpdateView.as_view(),name='lead-update'),
  path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
  path('<int:pk>/assign-agent/',AssignAgentView.as_view(),name='assign-agent'),

   path('category/', CategoryView.as_view(), name='category-view'),
   path('category/<int:pk>/',CategoryDetailView.as_view(),name='category-detail-view'),
   path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name='category-update-view'),
 
]