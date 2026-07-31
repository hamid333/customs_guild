from django.urls import path

from . import views

app_name = "specializations"

urlpatterns = [
    path("dashboard/specializations/", views.SpecializationDashListView.as_view(), name="dash_specialization_list"),
    path("dashboard/specializations/add/", views.SpecializationCreateView.as_view(), name="dash_specialization_add"),
    path("dashboard/specializations/<int:pk>/edit/", views.SpecializationUpdateView.as_view(), name="dash_specialization_edit"),
    path("dashboard/specializations/<int:pk>/delete/", views.SpecializationDeleteView.as_view(), name="dash_specialization_delete"),
]
