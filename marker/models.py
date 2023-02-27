from django.db import models

# Create your models here.
class Pothole(models.Model):

      pot_photo = models.FileField(upload_to='panthole')
      pot_description = models.TextField(max_length=255)
      pot_latitude = models.FloatField()
      pot_longitude = models.FloatField()
      status = models.BooleanField(default=False)