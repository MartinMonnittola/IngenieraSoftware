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
    game = models.ForeignKey(Partida, on_delete=models.CASCADE)
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    population_qty = models.IntegerField(default=0)
    missils_qty = models.IntegerField(default=0)
    shield_power = models.IntegerField(default=100)
    population_res = models.IntegerField(default=100)
    shield_res = models.IntegerField(default=0)
    missils_res = models.IntegerField(default=0)


class Bot(models.Model):
    strategy = (('Aggr', 'Aggressive'), ('Def', 'Defensive'))


class GameBot(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    game = models.ForeignKey(Partida, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField

    """ 
    Crea una partida en estado de espera. 
    """
    """ 
    def createPartida(): 
    """
    """ 
    Desactiva un planeta y elimina sus recursos 
    """
    """ 
    def deactivatePlanet(planet): 
    """
    """ 
     Comienza una partida  
    """
    """ 
    def startPartida(partida): 
    """

    """ 
    """
    """ 
    def joinPartida(partida, user): 
    """
    """ 
    Retorna la representacion del objeto en forma de string 
    """

    """ 
    def  __str__(self): 
      representation = (('User: %d '  % self.user) +  
                       ('initial_poblation: %d '  % self.initial_poblation) +  
                       ('const_misil: %d '  % self.const_misil) + 
                       ('const_shield: %d ' % self.const_shield) + 
                       ('const_poblation: %d ' % self.poblation) + 
                       ('time_misil: %d '  % self.time_misil) + 
                       ('hurt_to_poblation: %d '  % self.hurt_to_poblation) + 
                       ('hurt_to_poblation: %d '  % self.hurt_to_poblation)) 
      return representation 
    """

    """ 
    Metodos para realizar el testeo de la aplicacion. 
    """
    """ 
    def hurt_has_not_value_negative_or_zero(self): 
      self.assertGreater(self.hurt_to_shield, 0) 
      self.assertGreater(self.hurt_to_poblation, 0) 
    """
    """ 
    def const_has_not_value_negative_or_zero(self): 
      self.assertGreater(self.const_misil, 0) 
      self.assertGreater(self.const_poblation, 0) 
      self.assertGreater(self.const_shield, 0) 
    """
    """ 
    """

    """ 
    def time_misil_has_not_value_negative_or_zero(self): 
      self.assertGreater(self.time_misil, 0) 
    """
    """ 
    """
    """ 
    def initial_poblation_has_not_value_negative_or_zero(self): 
      self.assertGreater(self.time_poblation, 0) 
    """