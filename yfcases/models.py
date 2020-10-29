from django.db import models

class Yfcase(models.Model):
  yfcaseCaseNumber=models.CharField(u'案號(*)',max_length=100)

  def __str__(self):
    return self.yfcaseCaseNumber
