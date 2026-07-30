"""
مسیرهای اپ portal.
namespace: portal
"""
from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    # ---------------- صفحات عمومی ----------------
    path("", views.HomeView.as_view(), name="home"),
    path("members/", views.MemberListView.as_view(), name="member_list"),
    path("members/featured/", views.FeaturedMemberListView.as_view(), name="featured_members"),
    path("members/<int:pk>/", views.MemberDetailView.as_view(), name="member_detail"),
    path("hs-code/", views.HSCodeSearchView.as_view(), name="hs_code_search"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("works/", views.CompletedWorkListView.as_view(), name="completed_works"),
    path("contact/", views.ContactView.as_view(), name="contact"),

    # ---------------- داشبورد مدیریتی ----------------
    path("dashboard/login/", views.DashboardLoginView.as_view(), name="dashboard_login"),
    path("dashboard/logout/", views.DashboardLogoutView.as_view(), name="dashboard_logout"),
    path("dashboard/", views.DashboardHomeView.as_view(), name="dashboard_home"),
    #
    # # اعضا
    # path("dashboard/members/", views.MemberDashListView.as_view(), name="dash_member_list"),
    # path("dashboard/members/add/", views.MemberCreateView.as_view(), name="dash_member_add"),
    # path("dashboard/members/<int:pk>/edit/", views.MemberUpdateView.as_view(), name="dash_member_edit"),
    # path("dashboard/members/<int:pk>/delete/", views.MemberDeleteView.as_view(), name="dash_member_delete"),

    # اخبار
    path("dashboard/news/", views.NewsDashListView.as_view(), name="dash_news_list"),
    path("dashboard/news/add/", views.NewsCreateView.as_view(), name="dash_news_add"),
    path("dashboard/news/<int:pk>/edit/", views.NewsUpdateView.as_view(), name="dash_news_edit"),
    path("dashboard/news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="dash_news_delete"),

    # نمونه‌کارها
    path("dashboard/works/", views.WorkDashListView.as_view(), name="dash_work_list"),
    path("dashboard/works/add/", views.WorkCreateView.as_view(), name="dash_work_add"),
    path("dashboard/works/<int:pk>/edit/", views.WorkUpdateView.as_view(), name="dash_work_edit"),
    path("dashboard/works/<int:pk>/delete/", views.WorkDeleteView.as_view(), name="dash_work_delete"),

    # ردیف‌های تعرفه (HS Code)
    path("dashboard/hs-codes/", views.HSCodeDashListView.as_view(), name="dash_hscode_list"),
    path("dashboard/hs-codes/add/", views.HSCodeCreateView.as_view(), name="dash_hscode_add"),
    path("dashboard/hs-codes/<int:pk>/edit/", views.HSCodeUpdateView.as_view(), name="dash_hscode_edit"),
    path("dashboard/hs-codes/<int:pk>/delete/", views.HSCodeDeleteView.as_view(), name="dash_hscode_delete"),


    # اسلایدهای صفحه‌ی اصلی (HeroSlide)
    path("dashboard/slides/", views.SlideDashListView.as_view(), name="dash_slide_list"),
    path("dashboard/slides/add/", views.SlideCreateView.as_view(), name="dash_slide_add"),
    path("dashboard/slides/<int:pk>/edit/", views.SlideUpdateView.as_view(), name="dash_slide_edit"),
    path("dashboard/slides/<int:pk>/delete/", views.SlideDeleteView.as_view(), name="dash_slide_delete"),

    # پیام‌های تماس با ما
    path("dashboard/messages/", views.ContactMessageDashListView.as_view(), name="dash_message_list"),
    path("dashboard/messages/<int:pk>/", views.ContactMessageDetailView.as_view(), name="dash_message_detail"),
]
