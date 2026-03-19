from django.db.models.functions import TruncYear, TruncMonth
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Match
class MatchRatingView(APIView):

    def get(self,request):
         rating = (
             Match.objects
             .values(year=TruncYear('date'))
             .annotate(
             )
         )

