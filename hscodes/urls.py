from django.urls import path

from . import views

app_name = "hscodes"

urlpatterns = [
    path("hs-code/", views.HSCodeSearchView.as_view(), name="hs_code_search"),

    path("dashboard/hs-codes/", views.HSCodeDashListView.as_view(), name="dash_hscode_list"),
    path("dashboard/hs-codes/add/", views.HSCodeCreateView.as_view(), name="dash_hscode_add"),
    path("dashboard/hs-codes/<int:pk>/edit/", views.HSCodeUpdateView.as_view(), name="dash_hscode_edit"),
    path("dashboard/hs-codes/<int:pk>/delete/", views.HSCodeDeleteView.as_view(), name="dash_hscode_delete"),
]
