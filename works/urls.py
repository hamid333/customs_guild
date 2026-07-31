from django.urls import path

from . import views

app_name = "works"

urlpatterns = [
    path("works/", views.CompletedWorkListView.as_view(), name="completed_works"),

    path("dashboard/works/", views.WorkDashListView.as_view(), name="dash_work_list"),
    path("dashboard/works/add/", views.WorkCreateView.as_view(), name="dash_work_add"),
    path("dashboard/works/<int:pk>/edit/", views.WorkUpdateView.as_view(), name="dash_work_edit"),
    path("dashboard/works/<int:pk>/delete/", views.WorkDeleteView.as_view(), name="dash_work_delete"),
]
