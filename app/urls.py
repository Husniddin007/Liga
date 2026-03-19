from django.urls import path

from app.views import LeagueTableAPIView

urlpatterns = [
    path('rating/<int:season_id>/', LeagueTableAPIView.as_view()),
]