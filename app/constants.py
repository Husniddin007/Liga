from django.db import models

class FTRResult(models.IntegerChoices):
    H = 1,'h'
    D = 2,'d'
    A = 3,'a'
