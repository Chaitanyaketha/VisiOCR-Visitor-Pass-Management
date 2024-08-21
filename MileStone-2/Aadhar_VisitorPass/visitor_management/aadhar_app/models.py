from django.db import models

# Create your models here.

from django.db import models

class Aadhar(models.Model):
    aadhar_no = models.CharField(max_length=14)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=10)

    def __str__(self):
        return self.name
