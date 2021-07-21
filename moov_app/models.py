from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Furniture(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    type = models.CharField(max_length=25)
    color = models.CharField(max_length=12)
    user_id = models.IntegerField()

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('', kwargs={"furniture_id": self.id})

class FloorPlan(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    user_id = models.IntegerField()
    furnitures = models.ManyToManyField(Furniture)
    comment = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    