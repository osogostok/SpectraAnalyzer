from django.db import models
from django.contrib.auth.models import User


class Values(models.Model):
    type_spectr = models.CharField(max_length=3)
    values_x = models.TextField()
    values_y = models.TextField()


class Spectr(models.Model):
    file_name = models.TextField(unique=True)
    chemical_name = models.TextField(blank=True)

    values = models.ForeignKey(Values, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Спектр"
        verbose_name_plural = "Спектры"


class UsersSpectrs(models.Model):
    spectr = models.ForeignKey(Spectr, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_publish = models.BooleanField(default=True)
