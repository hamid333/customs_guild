from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),

    path("dashboard/news/", views.NewsDashListView.as_view(), name="dash_news_list"),
    path("dashboard/news/add/", views.NewsCreateView.as_view(), name="dash_news_add"),
    path("dashboard/news/<int:pk>/edit/", views.NewsUpdateView.as_view(), name="dash_news_edit"),
    path("dashboard/news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="dash_news_delete"),
]
