from django.db import models
from django.contrib.auth.models import User


"""
Modelo usado para almacenar los datos de la partida en espera o en curso.
"""
class Game(models.Model):

    # User creador de la partida.
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="User creator")
    initial_poblation =  models.IntegerField(default=1,
                                help_text="please enter values greater than 0.")
    const_misil = models.IntegerField(default=1, blank=False,
                                help_text="please enter values greater than 0.")
    const_shield = models.IntegerField(default=1, blank=False,
                                help_text="please enter values greater than 0.")
    const_poblation = models.IntegerField(default=1, blank=False,
                                help_text="please enter values greater than 0.")
    # Tiempo de viaje del misil.         
    time_misil = models.IntegerField(default=1, blank=False,
                    help_text="Please enter a number of minutes greater than 0")
    # Dano a la poblacion por misil.
    hurt_to_poblation = models.IntegerField(default=1, blank=False,
                    help_text="Please enter a percentage greater than 0")
    # Dano a la escudo por misil.
    hurt_to_shield = models.IntegerField(default=1, blank=False,
                           help_text="Please enter a percentage greater than 0")

    class Meta:
        ordering = ["user"]
        verbose_name_plural = "Games"

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
    def initial_poblation_has_not_value_negthenative_or_zero(self):
      self.assertGreater(self.initial_poblation, 0)
    """
