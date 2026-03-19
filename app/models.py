from django.db import models

from .constants import FTRResult


class Season(models.Model):
    name = models.CharField(max_length=20)
    division = models.CharField(max_length=10)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    class Meta:
        unique_together = ("name", "division")
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.name} ({self.division})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Match(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE, related_name="matches")
    home_team = models.ForeignKey(Team,on_delete=models.PROTECT,related_name="home_matches")
    away_team = models.ForeignKey(Team,on_delete=models.PROTECT, related_name="away_matches")
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL,null=True, blank=True,related_name="matches")

    date = models.DateField(db_index=True)

    fthg = models.SmallIntegerField(verbose_name="Full-time home goals")
    ftag = models.SmallIntegerField(verbose_name="Full-time away goals")
    ftr  = models.CharField(max_length=1, choices=FTRResult.choices, verbose_name="Full-time result")

    hthg = models.SmallIntegerField(null=True, blank=True, verbose_name="Half-time home goals")
    htag = models.SmallIntegerField(null=True, blank=True, verbose_name="Half-time away goals")
    hs = models.SmallIntegerField(null=True, blank=True, verbose_name="Home shots")
    a_s = models.SmallIntegerField(null=True, blank=True, verbose_name="Away shots",db_column="as")
    hst = models.SmallIntegerField(null=True, blank=True, verbose_name="Home shots on target")
    ast = models.SmallIntegerField(null=True, blank=True, verbose_name="Away shots on target")
    hf = models.SmallIntegerField(null=True, blank=True, verbose_name="Home fouls")
    af = models.SmallIntegerField(null=True, blank=True, verbose_name="Away fouls")
    hc = models.SmallIntegerField(null=True, blank=True, verbose_name="Home corners")
    ac = models.SmallIntegerField(null=True, blank=True, verbose_name="Away corners")
    hy = models.SmallIntegerField(null=True, blank=True, verbose_name="Home yellow cards")
    ay = models.SmallIntegerField(null=True, blank=True, verbose_name="Away yellow cards")
    hr = models.SmallIntegerField(null=True, blank=True, verbose_name="Home red cards")
    ar = models.SmallIntegerField(null=True, blank=True, verbose_name="Away red cards")



    class Meta:
        unique_together = ("season", "home_team", "away_team", "date")
        ordering = ["date"]
        indexes = [
            models.Index(fields=["season"]),
            models.Index(fields=["date"]),
            models.Index(fields=["home_team"]),
            models.Index(fields=["away_team"]),
        ]

    def __str__(self):
        return (
            f"{self.date} | {self.home_team} {self.fthg}–{self.ftag} {self.away_team}"
        )

    @property
    def home_result(self):
        return {"H": "W", "D": "D", "A": "L"}[self.ftr]

    @property
    def away_result(self):
        return {"H": "L", "D": "D", "A": "W"}[self.ftr]