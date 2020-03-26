from django.urls import path
from . import views

urlpatterns = [
    path('user/report/', views.ReportingUsersView.as_view()),
    path('user/recommend/', views.CreateShopRecommendationView.as_view()),
    path('user/recommend/update/', views.CreateShopRecommendationUpdateView.as_view())
]