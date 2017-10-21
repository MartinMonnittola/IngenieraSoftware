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
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Game user')

    # Nombre de la partida.
    game_name = models.CharField(max_length=20, verbose_name='Game Name',
                                 default='Default Name')

    # Tiempo en el que se inicio la partida.
    pub_date = models.DateTimeField(verbose_name='Date added')

    # Estado de la partida.
    game_started = models.BooleanField(default=0,
                                       verbose_name='Game started (True/False)')

    # Numero maximo de jugadores.
    max_players = models.IntegerField(default=0, 
                                      verbose_name='Game players limit',
                                      blank=True,
                                      validators=[MinValueValidator(2)])

    # Numero de jugadores que se unieron a la partida.
    connected_players = models.IntegerField(default=0,
                                        verbose_name='Amount of players online',
                                            validators=[MinValueValidator(0)])

    # Numero de bots que se agregaron a la partida a la partida.
    bot_players = models.IntegerField(default=2,
                                      verbose_name='Amount of bot players',
                                      validators=[MinValueValidator(2)])

    # Tiempo de viaje del misil.
    time_misil = models.IntegerField(default=1, verbose_name='Missile Delay',
                                     validators=[MinValueValidator(1)])

    # Poblacion inicial al comenzar la partida.
    initial_population = models.IntegerField(default=5000,
                                             verbose_name='Initial Population',
                                             validators=[MinValueValidator(0)])

    # Procentaje de poblacion asignado al recurso poblacion.
    const_population = models.IntegerField(default=1,
                                  verbose_name='Population Generation Constant',
                                           validators=[MinValueValidator(1)])

    # Procentaje de poblacion asignado al recurso escudo.
    const_shield = models.IntegerField(default=1,
                                      verbose_name='Shield Generation Constant',
                                       validators=[MinValueValidator(1)])

    # Procentaje de poblacion asignado al recurso misil.
    const_missile = models.IntegerField(default=1,
                                     verbose_name='Missile Generation Constant',
                                        validators=[MinValueValidator(1)])

    # Dano a la poblacion por misil.
    hurt_to_population = models.IntegerField(default=1,
                                   verbose_name='Population damage per missile',
                                             validators=[MinValueValidator(1)])

    # Dano a la escudo por misil.
    hurt_to_shield = models.IntegerField(default=1,
                                       verbose_name='Shield damage per missile',
                                         validators=[MinValueValidator(1)])

    def __str__(self):
        """ 
        Retorna la representacion del objeto en forma de string. 
        """
        representation = (('User: %d, '  % self.user.id) +
                         ('initial_poblation: %d, '  % self.initial_poblation) +  
                         ('const_misil: %d, '  % self.const_misil) + 
                         ('const_shield: %d, ' % self.const_shield) + 
                         ('const_poblation: %d, ' % self.const_poblation) + 
                         ('time_misil: %d, '  % self.time_misil) +
                         ('game_name: %s, '  % self.game_name) +
                         ('pub_date: %s, '  % 
                          self.pub_date.strftime("%Y-%m-%d %H:%M:%S")) +
                         ('game_started: %r, '  % self.game_started) +
                         ('max_players: %s, '  % self.max_players) +
                         ('bot_players: %s, '  % self.bot_players) +
                         ('connected_players: %s, '  % self.connected_players) +
                         ('game_name: %s, '  % self.game_name) +
                         ('hurt_to_poblation: %d, '  % self.hurt_to_poblation) + 
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
                 hurt_to_poblation, numero que indica el porcentaje de dano a la
                                    poblacion.
                 hurt_to_shield, numero que indica el porcentaje de dano a la
                                 escudo.
                 max_players, maximo numero de jugadores.
                 user, usuario creador de la partida.
        Salida: El Game creado.
        """
        game = cls(pub_date=timezone.now(),game_name=name,
                   max_players=max_players,game_started=False,user=owner)
        return game

    def joinGame(self, user_id, name):
        """
        Join Game:
        Procedure that allow players to join gameGames.
        INPUT: The game itself, the user who wants to join, and the planet name.
        OUTPUT: Boolean for succesfull or not join game action.
        """
        try:
            user = User.objects.get(pk=user_id)
            if Planet.objects.filter(game_started=0).exists():
                succesfull = False
            else:
                planet = Planet.create(user, self, name)
                self.connected_players += 1
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

    def deactivatePlanet(self, user_id):
        """ 
        Desactiva un planeta y elimina sus recursos.

        Entrada: planet_id, clave primaria del planeta.
        Salida:  succesfull, bool que indica si elimino el planeta.
        """
        try:
            planet = Planet.objects.get(player=user_id)
            planet.population_qty = 0
            planet.save()
            # Notificamo al usuario de la eliminacion de su planeta.
            #user.notify_devastation()
            succesfull = True
        except Planet.DoesNotExist:
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
    Planet Class: Contains all the information about each player's planet
    that will be generated after starting the game (in-game status).
    """
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    Game= models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name='Planet name')
    seed = models.BigIntegerField(default=0,verbose_name='Planet seed')
    population_qty = models.IntegerField(default=5000, verbose_name='Population Amout', validators=[MinValueValidator(0)])
    missiles_qty = models.IntegerField(default=0, verbose_name='Missile Amount', validators=[MinValueValidator(0)])
    shield_perc = models.IntegerField(default=100, verbose_name='Shield Amount', validators=[MinValueValidator(0)])
    population_distr = models.IntegerField(default=100, verbose_name='Planet Population %', validators=[MinValueValidator(0)])
    shield_distr = models.IntegerField(default=0,
                                       verbose_name='Planet Shield %',
                                       validators=[MinValueValidator(0)])
    missile_distr = models.IntegerField(default=0,
                                        verbose_name='Planet Missile %',
                                        validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, player, gameGame, name, seed):
        """
        Create Planet:
        Function that allow players to create their planets.
        INPUT: Planet attributes such as player owner, Gamethey belong to, name of the planet and a random seed.
        OUTPUT: A Planet Object.
        """
        new_planet = cls(player=player,gameGame=gameGame,name=name,population_qty=gameGame.initial_population,seed=seed)
        return new_planet

    def assign_perc_rate(self, perc_pop, perc_shield, perc_missile):
        if ((perc_pop + perc_shield + perc_missile) == 100):
            self.population_distr = perc_pop
            self.shield_distr = perc_shield
            self.missile_distr = perc_missile
        else:
            raise NameError('Wrong Distribution Choice')

    def decrease_shield(self, ammount):
        if (self.shield_perc >= ammount):
            self.shield_perc =- ammount
        else:
            self.shield_perc = 0

    def decrease_population(self, ammount):
        if (self.population_qty >= ammount):
            self.population_qty =- ammount
        else:
            self.population_qty = 0
