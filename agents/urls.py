from django.urls import path 
from .views import AgentListView,AgentCreateView,AgentDetailView,AgentUpdateView,AgentDeleteView

app_name = 'agents' # name of the app and also this is the name provided as namespace inside the main urls file in djcrm

urlpatterns = [
  path('',AgentListView.as_view(),name='agent-list'),
  path('create/',AgentCreateView.as_view(),name='agent-create'),
  path('<int:pk>/',AgentDetailView.as_view(),name='agent-detail'),
  path('<int:pk>/update/',AgentUpdateView.as_view(),name='agent-update'),
  path('<int:pk>/delete/',AgentDeleteView.as_view(),name='agent-delete'),
]