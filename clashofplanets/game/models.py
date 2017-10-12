from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Planet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    population_qty = models.IntegerField(default=0)
    missils_qty = models.IntegerField(default=0)
    shield_power = models.IntegerField(default=100)
    population_res = models.IntegerField(default=100)
    shield_res = models.IntegerField(default=0)
    missils_res = models.IntegerField(default=0)


class Game(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    population_init = models.IntegerField(default=0)
    population_const = models.IntegerField(default=0)
    missil_const = models.IntegerField(default=0)
    shield_const = models.IntegerField(default=0)
    missil_time = models.IntegerField(default=1)
    population_damage = models.IntegerField(default=0)
    shield_damage = models.IntegerField(default=0)


class Bot(models.Model):
    strategy = (('Aggr', 'Aggressive'), ('Def', 'Defensive'))


class GameBot(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField