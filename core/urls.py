from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("dashboard/login/", views.DashboardLoginView.as_view(), name="dashboard_login"),
    path("dashboard/logout/", views.DashboardLogoutView.as_view(), name="dashboard_logout"),
    path("dashboard/", views.DashboardHomeView.as_view(), name="dashboard_home"),

    # مدیریت کاربران داشبورد + دسترسی بخش‌ها
    path("dashboard/users/", views.UserDashListView.as_view(), name="dash_user_list"),
    path("dashboard/users/add/", views.UserCreateView.as_view(), name="dash_user_add"),
    path("dashboard/users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="dash_user_edit"),
    path("dashboard/users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="dash_user_delete"),
]
