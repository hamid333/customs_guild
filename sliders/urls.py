from django.urls import path

from . import views

app_name = "sliders"

urlpatterns = [
    path("dashboard/slides/", views.SlideDashListView.as_view(), name="dash_slide_list"),
    path("dashboard/slides/add/", views.SlideCreateView.as_view(), name="dash_slide_add"),
    path("dashboard/slides/<int:pk>/edit/", views.SlideUpdateView.as_view(), name="dash_slide_edit"),
    path("dashboard/slides/<int:pk>/delete/", views.SlideDeleteView.as_view(), name="dash_slide_delete"),
]
