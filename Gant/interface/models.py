from django.db import models

# Create your models here.


class Interface(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

class Base(models.Model):
    detail_number = models.IntegerField()
    detail_stanok_number = models.IntegerField()
    detail_time = models.IntegerField()

    def __str__(self):
        return f"{self.detail_number} {self.detail_stanok_number} {self.detail_time}"

    class Meta:
        verbose_name='Деталь'
        verbose_name_plural='Детали'


