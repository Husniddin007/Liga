from rest_framework import serializers


class LeagueTableSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    team = serializers.CharField()
    played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    points = serializers.IntegerField()
    form = serializers.CharField()
