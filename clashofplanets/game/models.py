from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User creador de la partida
    initial_poblation = models.IntegerField(default=1)
    const_misil = models.IntegerField(default=1, blank=False)
    const_shield = models.IntegerField(default=1, blank=False)
    const_poblation = models.IntegerField(default=1, blank=False)
    time_misil = models.IntegerField(default=1, blank=False)  # Tiempo de viaje del misil
    hurt_to_poblation = models.IntegerField(default=1, blank=False)  # Dano a la poblacion por misil
    hurt_to_shield = models.IntegerField(default=1, blank=False)  # Dano a la escudo por misil


# Create your models here.
class Planet(models.Model):
    game = models.ForeignKey(Partida, on_delete=models.CASCADE, default=0)
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    population_qty = models.IntegerField(default=0)
    missils_qty = models.IntegerField(default=0)
    shield_power = models.IntegerField(default=100)
    population_res = models.IntegerField(default=100)
    shield_res = models.IntegerField(default=0)
    missils_res = models.IntegerField(default=0)

