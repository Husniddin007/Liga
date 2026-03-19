from django.db import models

from .constants import FTRResult


class Team(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Referee(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=128,unique=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    div = models.ForeignKey(Division, on_delete=models.PROTECT,related_name='match')
    referee = models.ForeignKey(Referee, on_delete=models.PROTECT,related_name='referee')
    date = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT,related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT,related_name='away_team')
    fthg = models.SmallIntegerField(verbose_name='uy toliq vaqt gol ')
    ftag = models.SmallIntegerField(verbose_name='mehmon toliq vaqt gol ')
    ftr = models.CharField(choices=FTRResult.choices)
    hthg = models.SmallIntegerField(verbose_name='uy yarim vaqt gol ')
    htag = models.SmallIntegerField(verbose_name='mehmon yarim vaqt gol ')
    hs = models.SmallIntegerField(verbose_name='uy zarbalar soni ')
    a_s = models.SmallIntegerField(verbose_name='mehmon zarbalar soni ')
    hst = models.SmallIntegerField(verbose_name='uy aniq zarbalar soni ')
    ast = models.SmallIntegerField(verbose_name='mehmon aniq zarbalar soni ')
    hf = models.SmallIntegerField(verbose_name='uy follar ')
    af = models.SmallIntegerField(verbose_name='mehmon follar ')
    hc = models.SmallIntegerField(verbose_name='uy burchak zarbalar soni ')
    ac = models.SmallIntegerField(verbose_name='mehmon burchak soni ')
    hy = models.SmallIntegerField(verbose_name='uy sariq soni ')
    ay = models.SmallIntegerField(verbose_name='mehmon sariq soni ')
    hr = models.SmallIntegerField(verbose_name='uy qizil soni ')
    ar = models.SmallIntegerField(verbose_name='mehmon qizil soni ')

    def __str__(self):
        return self.div




