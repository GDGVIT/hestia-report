from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.ReportingUsersView.as_view()),
    path('recommend/', views.CreateShopRecommendationView.as_view()),
    path('recommend/update/', views.CreateShopRecommendationUpdateView.as_view())
]