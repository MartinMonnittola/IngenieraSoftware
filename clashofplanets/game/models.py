# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Game(models.Model):
    """
    Game Class: Contains all the information about a game lobby (pre-game status).
    """
    # User creador de la partida.
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Game user')
    # Nombre de la partida.
    game_name = models.CharField(max_length=20, verbose_name='Game Name', default='Default Name')
    # Tiempo en el que se inicio la partida.
    pub_date = models.DateTimeField(verbose_name='Date added')
    # Estado de la partida.
    game_started = models.BooleanField(default=0,verbose_name='Game started (True/False)')
    # Numero maximo de jugadores.
    max_players = models.IntegerField(default=0, verbose_name='Game players limit',blank=True,validators=[MinValueValidator(2)])
    # Numero de jugadores que se unieron a la partida.
    connected_players = models.IntegerField(default=0,verbose_name='Amount of players online',validators=[MinValueValidator(0)])
    # Numero de bots que se agregaron a la partida a la partida.
    bot_players = models.IntegerField(default=2, verbose_name='Amount of bot players',validators=[MinValueValidator(2)])
    # Tiempo de viaje del misil.
    time_misil = models.IntegerField(default=1, verbose_name='Missile Delay',validators=[MinValueValidator(1)])
    # Poblacion inicial al comenzar la partida.
    initial_population = models.IntegerField(default=5000,verbose_name='Initial Population',validators=[MinValueValidator(0)])
    # Procentaje de poblacion asignado al recurso poblacion.
    const_population = models.IntegerField(default=1,verbose_name='Population Generation Constant',validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso escudo.
    const_shield = models.IntegerField(default=1,verbose_name='Shield Generation Constant',validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso misil.
    const_missile = models.IntegerField(default=1,verbose_name='Missile Generation Constant',validators=[MinValueValidator(1)])
    # Daño a la poblacion por misil.
    hurt_to_population = models.IntegerField(default=1, verbose_name='Population damage per missile',validators=[MinValueValidator(1)])
    # Daño a la escudo por misil.
    hurt_to_shield = models.IntegerField(default=1,verbose_name='Shield damage per missile',validators=[MinValueValidator(1)])

    def __str__(self):
        """
        Retorna la representacion del objeto en forma de string.
        """
        representation = (('User: %d, '  % self.user.id) +
                         ('initial_poblation: %d, '  % self.initial_population) +
                         ('const_misil: %d, '  % self.const_missile) +
                         ('const_shield: %d, ' % self.const_shield) +
                         ('const_poblation: %d, ' % self.const_population) +
                         ('time_misil: %d, '  % self.time_misil) +
                         ('game_name: %s, '  % self.game_name) +
                         ('pub_date: %s, '  %
                          self.pub_date.strftime("%Y-%m-%d %H:%M:%S")) +
                         ('game_started: %r, '  % self.game_started) +
                         ('max_players: %s, '  % self.max_players) +
                         ('bot_players: %s, '  % self.bot_players) +
                         ('connected_players: %s, '  % self.connected_players) +
                         ('game_name: %s, '  % self.game_name) +
                         ('hurt_to_population: %d, '  % self.hurt_to_population) +
                         ('hurt_to_shield: %d'  % self.hurt_to_shield))
        return representation

    @classmethod
    def create(cls, owner, name, max_players):
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
                 hurt_to_population, numero que indica el porcentaje de daño a la
                                    poblacion.
                 hurt_to_shield, numero que indica el porcentaje de daño a la
                                 escudo.
                 max_players, maximo numero de jugadores.
                 user, usuario creador de la partida.
        Salida: El Game creado.
        """
        game = cls(pub_date=timezone.now(),game_name=name,
                   max_players=max_players,
                   game_started=False,
                   user=owner)
        #game.save
        return game

    def joinGame(self, user_id, name, seed):
        """
        Join Game:
        Procedure that allow players to join gameGames.
        INPUT: The game itself, the user who wants to join, and the planet name.
        OUTPUT: Boolean for succesfull or not join game action.
        """
        try:
            user = User.objects.get(pk=user_id)
            if Planet.objects.filter(player=user, game=self).exists():
                succesfull = False
            else:
                planet = Planet.create(user, self, name, seed)
                planet.save()
                self.connected_players += 1
                self.save()
                succesfull = True
        except User.DoesNotExist:
            succesfull = False
        return succesfull

    def startGame(self):
        """
        Marca como iniciada una partida.

        Entrada: self, el objeto game.
        Salida:  nada.
        """
        if not (self.game_started):
            self.game_started = True
            self.save()

    def desactivatePlanet(self, planet_id):
        """
        Desactiva un planeta y elimina sus recursos.

        Entrada: planet_id, clave primaria del planeta.
        Salida:  succesfull, bool que indica si elimino el planeta.
        """
        try:
            planet = Planet.objects.get(pk=planet_id, game=self)
            if planet.population_qty != 0:
                planet.population_qty = 0
                planet.save()
                succesfull = True                
            else:
                succesfull = False
            # Notificamo al usuario de la eliminacion de su planeta.
            #user.notify_devastation()
        except Planet.DoesNotExist, User.DoesNotExist:
            succesfull = False
        return succesfull

    """
    DeleteGame:
    Procedure that allows the gameGame owner to delete theGame.
    INPUT: Owner user id.
    OUTPUT: Boolean for succesfull or not delete gameGame object.
    """
    """"
    def delete(self, user_id):
        try:
            Game =Game.objects.get(owner=user_id)
            game_owner =Game.owner
            Game.deactivatePlanet(game_owner)
            Game.delete()
            succesfull = True
        except Game.DoesNotExist:
            succesfull = False
        return succesfull
    """

class Planet(models.Model):
    """
    Clase Planet: Contiene toda la informacion acerca del planeta de cada
    jugador que sera generado luego de comenzado el juego (estado in-game)
    """
    player = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='Default Name', verbose_name='Planet name')
    seed = models.BigIntegerField(default=0,verbose_name='Planet seed')
    population_qty = models.IntegerField(default=5000, verbose_name='Population Amout', validators=[MinValueValidator(0)])
    missiles_qty = models.IntegerField(default=0, verbose_name='Missile Amount', validators=[MinValueValidator(0)])
    shield_perc = models.IntegerField(default=100, verbose_name='Shield Amount', validators=[MinValueValidator(0)])
    population_distr = models.IntegerField(default=100, verbose_name='Planet Population %', validators=[MinValueValidator(0)])
    shield_distr = models.IntegerField(default=0,verbose_name='Planet Shield %',validators=[MinValueValidator(0)])
    missile_distr = models.IntegerField(default=0,verbose_name='Planet Missile %',validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, player, game, name, seed):
        """
        Create Planet:
        Permite a los jugadores crear sus planetas
        INPUT: Dueño del planeta, partida a la que pertenece,
               nombre del planeta y un seed al azar
        OUTPUT: Objeto Planet
        """
        new_planet = cls(player=player,game=game,name=name,population_qty=game.initial_population,seed=seed)
        return new_planet

    def assign_perc_rate(self, perc_pop, perc_shield, perc_missile):
        """
        Assign percentage rates:
        Asigna los porcentajes de trabajo sobre cada recurso del planeta
        INPUT: Objeto Planet, Integers para el porcentaje dedicado a poblacion,
               generacion de escudo, y creacion de misiles
        OUTPUT: Ninguno
        """
        if ((perc_pop + perc_shield + perc_missile) == 100):
            self.population_distr = perc_pop
            self.shield_distr = perc_shield
            self.missile_distr = perc_missile
        else:
            raise NameError('Wrong Distribution Choice')

    def decrease_shield(self, ammount):
        """
        Decrease shield:
        Dana el escudo del planeta
        INPUT: Objeto Planet, cantidad de daño
        OUTPUT: Ninguno
        """
        if (ammount <= 100):
            if (self.shield_perc >= ammount):
                self.shield_perc =- ammount
            else:
                self.shield_perc = 0
        else:
            raise NameError('Wrong ammount of damage. Must be 100 or less')

    def decrease_population(self, ammount):
        """
        Decrease population:
        Dana la poblacion del planeta
        INPUT: Objeto Planet, cantidad de daño
        OUTPUT: Ninguno
        """
        if (self.population_qty >= ammount):
            self.population_qty =- ammount
        else:
            self.population_qty = 0

    def launch_missile(self, enemy_planet):
        """
        Launch missile:
        Crea un objeto Missile dirigido a un planeta objetivo
        INPUT: Objeto Planet, planeta enemigo
        OUTPUT: Bool que indica si pudo enviarse el misil
        """
        if (self.missiles_qty >= 0):
            try:
                missile = Missile(owner=self, target=enemy_planet)
                missile.save()
                self.missiles_qty =- 1
                missile_launched = True
            except Missile.DoesNotExist:
                missile_launched = False
        else:
            missile_launched = False

        return missile_launched


    def get_missiles_state(self):
        """
        Get missiles state:
        Examina cada objeto Missile y obtiene el tiempo para impacto de cada uno
        INPUT: Objeto Planet
        OUTPUT: Diccionario con nombre de planetas y correspondientes tiempos de impacto
        """
        missiles = Missile.objects.all(owner=self)
        times = {}

        for missile in missiles:
            times[missile.target.name] = missile.time_to_target()

        return times


class Missile (models.Model):
    """
    Clase Missile: Contiene el planeta origen, planeta destino, y hora de lanzamiento
    """
    owner = models.ForeignKey(Planet, related_name="owner")
    target = models.ForeignKey(Planet, related_name="target")
    launch_time = models.DateTimeField(auto_now_add=True)

    def deal_damage(self):
        """
        Deal damage:
        Calcula el daño a escudo y poblacion del planeta enemigo
        INPUT: Objeto Missile
        OUTPUT: Ninguno
        """
        target_planet = self.target
        gameroom = target_planet.gameroom

        if (target_planet.shield_perc == 0):
            damage = gameroom.population_damage_per_missile
        else:
            damage_diminisher = (100 / target_planet.shield_perc)
            damage = gameroom.population_damage_per_missile / damage_diminisher

        target_planet.decrease_shield(gameroom.shield_damage_per_missile)
        target_planet.decrease_population(damage)

    def time_to_target(self):
        """
        Time to target:
        Calcula el tiempo restante para el impacto
        INPUT: Objeto Missile
        OUTPUT: Tiempo para el impacto
        """
        gameroom = self.owner.gameroom
        time_elapsed = self. launch_time - timezone.datetime.now()
        time_to_impact = gameroom.missile_delay - time_elapsed

        return time_to_impact
