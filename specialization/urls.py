from django.urls import path
from . import views


urlpatterns = [
    path("", views.SpecializationDashListView.as_view(), name="specialization_list"),
    path("add/", views.SpecializationCreateView.as_view(), name="specialization_add"),
    path("<int:pk>/edit/", views.SpecializationUpdateView.as_view(), name="specialization_edit"),
    path("<int:pk>/delete/", views.SpecializationDeleteView.as_view(), name="specialization_delete"),
]
