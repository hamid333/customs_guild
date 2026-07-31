from django.urls import path

from . import views

app_name = "contact"

urlpatterns = [
    path("contact/", views.ContactView.as_view(), name="contact"),

    path("dashboard/messages/", views.ContactMessageDashListView.as_view(), name="dash_message_list"),
    path("dashboard/messages/<int:pk>/", views.ContactMessageDetailView.as_view(), name="dash_message_detail"),
]
