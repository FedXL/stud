from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser, User


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


class ArchiveLetter(models.Model):
    explain = models.TextField(null=True, blank=True)
    method = models.TextField()
    rating = models.TextField()
    details = models.IntegerField()
    tools = models.IntegerField()
    series = models.IntegerField()
    name = models.ForeignKey(User, on_delete=models.CASCADE)


class ArchiveData(models.Model):
    detail_number = models.IntegerField()
    detail_tools_number = models.IntegerField()
    detail_time = models.IntegerField()
    record_number = models.ForeignKey(ArchiveLetter, on_delete=models.CASCADE)


class Settings(models.Model):
    spt_ltp = models.FloatField()
    lukr_mwkr = models.FloatField()
    fopnr_anti = models.FloatField()
    name = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)