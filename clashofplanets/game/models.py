from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

"""
Modelo usado para almacenar los datos de la partida en espera o en curso.
"""
class Partida(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)          # User creador de la partida
  initial_poblation =  models.IntegerField(default=1)
  const_misil = models.IntegerField(default=1, blank=False)
  const_shield = models.IntegerField(default=1, blank=False)
  const_poblation = models.IntegerField(default=1, blank=False)          
  time_misil = models.IntegerField(default=1, blank=False)          # Tiempo de viaje del misil
  hurt_to_poblation = models.IntegerField(default=1,blank=False)    # Dano a la poblacion por misil
  hurt_to_shield = models.IntegerField(default=1, blank=False)      # Dano a la escudo por misil


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

"""
Modelo usado para almacenar datos de cada planeta
"""
class Planet(models.Model):

  player = models.ForeignKey(User, on_delete=models.CASCADE)
  gameroom = models.ForeignKey(Partida, on_delete=models.CASCADE)
# bot = models.ForeignKey(Bot)
  name = models.CharField(max_length=200, blank=False)
  population_amm = models.IntegerField(default=5000, blank=False,
                                       validators=[MinValueValidator(0)])
  missile_amm = models.IntegerField(default=0, blank=False)
  shield_perc = models.IntegerField(default=0, blank=False)
  population_distr = models.IntegerField(default=100, blank=False,
                                         validators=[MinValueValidator(0)])
  shield_distr = models.IntegerField(default=0, blank=False,
                                     validators=[MinValueValidator(0)])
  missile_distr = models.IntegerField(default=0, blank=False,
                                      validators=[MinValueValidator(0)])

  @classmethod
  def create(cls, player, gameroom, name):
    new_planet = cls(player=player,
                     gameroom=gameroom,
                     name=name,
                     population_amm=gameroom.init_population)
    return new_planet

  
  def assign_perc_rate(self, perc_pop, perc_shield, perc_missile):
    if ((perc_pop + perc_shield + perc_missile) == 100):
      self.population_distr = perc_pop
      self.shield_distr = perc_shield
      self.missile_distr = perc_missile
    else:
      raise NameError('Porcentajes erroneos')


  def decrease_shield(self, ammount):
    if (self.shield_perc >= ammount):
      self.shield_perc =- ammount
    else:
      self.shield_perc = 0


  def decreace_population(self, ammount):
    if (self.population_amm >= ammount):
      self.population_amm =- ammount
    else:
      self.population_amm = 0  

  """
  Retorna la representacion del objeto en forma de string
  """
  def  __str__(self):
    representation = (('player: %d ' % self.player) + 
                      ('gameroom: %d ' % self.gameroom) + 
                      ('name: %d ' % self.name) +
                      ('population_amm: %d ' % self.population_amm) +
                      ('missile_amm: %d ' % self.missile_amm) +
                      ('shield_perc: %d ' % self.shield_perc) +
                      ('population_distr: %d ' % self.population_distr) +
                      ('shield_distr: %d ' % self.shield_distr) +
                      ('missile_distr: %d ' % self.missile_distr))
    return representation