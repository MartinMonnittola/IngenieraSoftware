from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


""" 
Modelo usado para almacenar los datos de la partida en espera o en curso. 
"""
class Game(models.Model):

    # User creador de la partida.
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="User creator")

    # Poblacion inicial al comenzar la partida.
    initial_poblation =  models.IntegerField(default=1,
                                help_text="please enter values greater than 0.")

    # Procentaje de poblacion asignado al recurso misil.
    const_misil = models.IntegerField(default=1, blank=False,
                                help_text="please enter values greater than 0.")

    # Procentaje de poblacion asignado al recurso escudo.
    const_shield = models.IntegerField(default=1, blank=False,
                                help_text="please enter values greater than 0.")

    # Procentaje de poblacion asignado al recurso poblacion.
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

    # Numero maximo de jugadores.
    max_players = models.IntegerField(default=2)

    # Estado de la partida.
    playing = models.BooleanField(default=False)

    class Meta:
        ordering = ["user"]
        verbose_name_plural = "Games"

    """ 
    Crea una partida en estado de espera. 
    Entrada: Gm, Clase Game.
             initial_poblation, numero que indica la poblacion inicial.
             const_misil, pocentaje que indica el pocentaje de pobladores
                          asignado al recurso misil.
             const_shield, pocentaje que indica el pocentaje de pobladores
                          asignado al recurso escudo.
             const_poblation, pocentaje que indica el pocentaje de pobladores
                          asignado al recurso poblacion.
             time_misil, tiempo que tarda el misil en llegar al planeta atacado.
             hurt_to_poblation, numero que indica el porcentaje de dano a la
                                poblacion.
             hurt_to_shield, numero que indica el porcentaje de dano a la
                             escudo.
             max_players, maximo numero de jugadores.
             user, usuario creador de la partida.
    Salida: El Game creado.
    """
    @classmethod
    def createGame(Gm, initial_poblation, const_misil,
                  const_shield, const_poblation,
                  time_misil, hurt_to_poblation,
                  hurt_to_shield, max_players, user):
        game = Gm(initial_poblation=initial_poblation, const_misil=const_misil,
                  const_shield=const_shield, const_poblation=const_poblation,
                  time_misil=time_misil, hurt_to_poblation=hurt_to_poblation,
                  hurt_to_shield=hurt_to_shield, max_players=max_players,
                  playing=False, user=user)
        return game

    """ 
    Desactiva un planeta y elimina sus recursos. Se puede ejecutar antes de
    empezar la patida o en el tanscurso de esta.
    Entrada: planet_id, clave primaria del planeta.
    Salida:  succesfull, bool que indica si elimino el planeta.
    """
    def deactivatePlanet(self, planet_id):
        try:
            planet = Planet.objects.get(pk=planet_id)
            user = planet.player
            planet.delete()
            # Notificamo al usuario de la eliminacion de su planeta.
            #user.notify_devastation()
            succesfull = True
        except Planet.DoesNotExist:
            succesfull = False
        return succesfull

    """ 
    Marca como iniciada una partida.
    """
    def startPartida(self):
        self.playing = True

    """ 
    Unirse a una partida.
    Entrada: user_id, el id del usuario.
             name, el nombre del planeta.
    Salida:  succesfull, bool que indica si el usuario se unio a la partida.
    """
    def joinGame(user_id, name):
        try:
           user = User.objects.get(pk=user_id)
           planet = Planet.create(Planet, user, self, name)
           succesfull = True
        except User.DoesNotExist:
            succesfull = False
        return succesfull

    """ 
    Retorna la representacion del objeto en forma de string. 
    """
    def  __str__(self): 
        representation = (('User: %d, '  % self.user.id) +
                         ('initial_poblation: %d, '  % self.initial_poblation) +  
                         ('const_misil: %d, '  % self.const_misil) + 
                         ('const_shield: %d, ' % self.const_shield) + 
                         ('const_poblation: %d, ' % self.const_poblation) + 
                         ('time_misil: %d, '  % self.time_misil) + 
                         ('hurt_to_poblation: %d, '  % self.hurt_to_poblation) + 
                         ('hurt_to_poblation: %d'  % self.hurt_to_poblation)) 
        return representation 


"""
Modelo usado para almacenar datos de cada planeta
"""
class Planet(models.Model):

  player = models.ForeignKey(User, on_delete=models.CASCADE)
  gameroom = models.ForeignKey(Game, on_delete=models.CASCADE)
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
                     population_amm=gameroom.initial_poblation)
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

