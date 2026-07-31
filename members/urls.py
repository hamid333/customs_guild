from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path("members/", views.MemberListView.as_view(), name="member_list"),
    path("members/featured/", views.FeaturedMemberListView.as_view(), name="featured_members"),
    path("members/<int:pk>/", views.MemberDetailView.as_view(), name="member_detail"),

    path("dashboard/members/", views.MemberDashListView.as_view(), name="dash_member_list"),
    path("dashboard/members/add/", views.MemberCreateView.as_view(), name="dash_member_add"),
    path("dashboard/members/<int:pk>/edit/", views.MemberUpdateView.as_view(), name="dash_member_edit"),
    path("dashboard/members/<int:pk>/delete/", views.MemberDeleteView.as_view(), name="dash_member_delete"),
]
