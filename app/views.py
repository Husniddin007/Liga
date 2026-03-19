from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from app.serializers import LeagueTableSerializer
from .models import Team, Season
from .services import get_team_season_stats


class LeagueTableAPIView(APIView):
    @extend_schema(responses={200: LeagueTableSerializer})
    def get(self, request, season_id):
        season = get_object_or_404(Season, id=season_id)
        teams = Team.objects.all()

        all_stats = []
        for team in teams:
            stats = get_team_season_stats(team, season)
            all_stats.append(stats)

        all_stats.sort(key=lambda x: (-x['points'], -x['goal_diff']))

        search_query = request.query_params.get('search', '').lower()
        if search_query:
            all_stats = [item for item in all_stats if search_query in item['team'].lower()]

        order_by = request.query_params.get('ordering', 'points')

        reverse = True
        if order_by.startswith('-'):
            order_by = order_by[1:]
            reverse = False

        if order_by == 'points':
            all_stats.sort(key=lambda x: (-x['points'], -x['goal_diff']))
        else:
            all_stats.sort(key=lambda x: x.get(order_by, 0), reverse=reverse)

        for index, item in enumerate(all_stats, start=1):
            item['rank'] = index

        serializer = LeagueTableSerializer(all_stats, many=True)
        return Response(serializer.data)


