from django.db import models
from django.contrib.sessions.models import Session


# Create your models here.



class Base(models.Model):

    detail_number = models.IntegerField()
    detail_stanok_number = models.IntegerField()
    detail_time = models.IntegerField()
    detail_turn = models.IntegerField(null=True, blank=True)
    redis = models.ForeignKey(Session, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.detail_number} {self.detail_stanok_number} {self.detail_time}"

    class Meta:
        verbose_name='Деталь'
        verbose_name_plural='Детали'


class Vocabulary(models.Model):
    series = models.IntegerField(null=True, blank=True)
    methods = models.TextField(null=True, blank=True)
    details = models.IntegerField(null=True, blank=True)
    tools = models.IntegerField(null=True, blank=True)
    redis = models.OneToOneField(Session, on_delete=models.CASCADE, primary_key=True)


