from django.urls import path
from . import views


urlpatterns = [
    # اسلایدهای صفحه‌ی اصلی (HeroSlide)
    path("", views.SlideDashListView.as_view(), name="slide_list"),
    path("add/", views.SlideCreateView.as_view(), name="slide_add"),
    path("<int:pk>/edit/", views.SlideUpdateView.as_view(), name="slide_edit"),
    path("<int:pk>/delete/", views.SlideDeleteView.as_view(), name="slide_delete"),

]
