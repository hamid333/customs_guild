from django.urls import path
from . import views


urlpatterns = [
    path("", views.MemberDashListView.as_view(), name="member_list"),
    path("add/", views.MemberCreateView.as_view(), name="member_add"),
    path("<int:pk>/edit/", views.MemberUpdateView.as_view(), name="member_edit"),
    path("<int:pk>/delete/", views.MemberDeleteView.as_view(), name="member_delete"),

]
