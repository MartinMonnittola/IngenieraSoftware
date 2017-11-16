# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import numpy
import random
from haikunator import Haikunator

class Game(models.Model):
    """
    Clase Game contiene informacion sobre las partidas en espera y en ejecucion.
    """
    # User creador de la partida.
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Game user')
    # Nombre de la partida.
    game_name = models.CharField(max_length=20,
                                 verbose_name='Game Name',
                                 default='Default Name')
    # Tiempo en el que se inicio la partida.
    pub_date = models.DateTimeField(verbose_name='Date added',
                                    default=timezone.now)
    # Estado de la partida.
    game_started = models.BooleanField(
                                      default=0,
                                      verbose_name='Game started (True/False)')
    # Numero de alianzas
    num_alliances = models.IntegerField(default=0,
                                      verbose_name='Number of Alliances',
                                      blank=True,
                                      validators=[MinValueValidator(0)])
    # Numero maximo de jugadores.
    max_players = models.IntegerField(default=0,
                                      verbose_name='Game players limit',
                                      blank=True,
                                      validators=[MinValueValidator(2)])
    # Numero de jugadores que se unieron a la partida.
    connected_players = models.IntegerField(default=0,
                                            verbose_name='Connected players',
                                            validators=[MinValueValidator(0)])
    # Numero de bots que se agregaron a la partida a la partida.
    bot_players = models.IntegerField(default=0,
                                      verbose_name='Amount of bot players',
                                      validators=[MinValueValidator(0)])
    # Tiempo de viaje del misil.
    time_missile = models.IntegerField(default=1,
                                       verbose_name='Missile Delay',
                                       validators=[MinValueValidator(1)])
    # Poblacion inicial al comenzar la partida.
    initial_population = models.IntegerField(default=5000,
                                             verbose_name='Initial Population',
                                             validators=[MinValueValidator(0)])
    # Procentaje de poblacion asignado al recurso poblacion.
    const_population = models.IntegerField(
                                  default=1,
                                  verbose_name='Population Genration Constant',
                                  validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso escudo.
    const_shield = models.IntegerField(
                                     default=1,
                                     verbose_name='Shield Generation Constant',
                                     validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso misil.
    const_missile = models.IntegerField(
                                    default=1,
                                    verbose_name='Missile Generation Constant',
                                    validators=[MinValueValidator(1)])
    # Daño a la poblacion por misil.
    hurt_to_population = models.IntegerField(
                                  default=1,
                                  verbose_name='Population damage per missile',
                                  validators=[MinValueValidator(1)])
    # Daño a la escudo por misil.
    hurt_to_shield = models.IntegerField(
                                      default=1,
                                      verbose_name='Shield damage per missile',
                                      validators=[MinValueValidator(1)])

    def __str__(self):
        """
        Retorna la representacion del objeto en forma de string.
        """
        representation = (('User: %d, ' % self.user.id) +
                          ('initial_poblation: %d, ' %
                           self.initial_population) +
                          ('const_misil: %d, ' % self.const_missile) +
                          ('const_shield: %d, ' % self.const_shield) +
                          ('const_poblation: %d, ' % self.const_population) +
                          ('time_missile: %d, ' % self.time_missile) +
                          ('game_name: %s, ' % self.game_name) +
                          ('pub_date: %s, ' %
                           self.pub_date.strftime("%Y-%m-%d %H:%M:%S")) +
                          ('game_started: %r, ' % self.game_started) +
                          ('max_players: %s, ' % self.max_players) +
                          ('bot_players: %s, ' % self.bot_players) +
                          ('connected_players: %s, ' %
                           self.connected_players) +
                          ('game_name: %s, ' % self.game_name) +
                          ('hurt_to_population: %d, ' %
                           self.hurt_to_population) +
                          ('hurt_to_shield: %d' % self.hurt_to_shield))
        return representation

    @classmethod
    def create(cls, owner, name, max_players):
        """
        Crea una partida en estado de espera.

        Entrada: cls, Clase Game.
                 game_name, nombre del partida.
                 owner, usurio creador del partida.
                 max_players, maximo numero de jugadores.
        Salida: game,  objeto Game creado.
        """
        game = cls(pub_date=timezone.now(),
                   game_name=name,
                   max_players=max_players,
                   game_started=False,
                   user=owner)
        game.connected_players += 1
        return game

    def joinGame(self, user_id, name, seed):
        """
        Une a un usuario al usuario a la partida.

        Entrada: self, el objeto partida mismo.
                 user_id, entero que representa la clave primaria del user
                          que se unira a la partida.
                 name, nombre del planeta que se creara para el usuario con
                       pk user_id.
                 seed, clave de session.
        Salida:  bool que indica si el usuario pudo unirse a la partida.
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
        Salida:  bool que indica si elimino el planeta.
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
            # user.notify_devastation()
        except (Planet.DoesNotExist, User.DoesNotExist):
            succesfull = False
        return succesfull

class Bot(models.Model):
    # Probabilidad de decidir atacar.
    probability_attack = models.IntegerField(default=30,
                                      help_text='probability of attack',
                                      blank=False)

    # Probabilidad de decidir modificar los recursos.
    probability_modify_resources = models.IntegerField(default=60,
                                 help_text='probability of modifying resources',
                                 blank=False)

    # Probabilidad de decidir esperar y no realizar acciones.
    probability_not_acting = models.IntegerField(default=10,
                                 help_text='probability of not acting',
                                 blank=False)

    # Partida a la que pertenece el bot.
    game = models.ForeignKey(Game, default = 1, on_delete = models.CASCADE)

    # Nombre del bot.
    name = models.CharField(max_length=20, blank=False, verbose_name='Bot name')

    """
    Clase abstracta que representa a los bot.
    """
    def attack(self):
        """
        Decide aleatoriamente si ataca a uno o mas planetas.
        """
        pass

    def defense(self):
        """
        Decide aleatoriamente si modifica los recursos del planeta propio.
        """
        pass



class Planet(models.Model):
    """
    Clase Planet: Contiene toda la informacion acerca del planeta de cada
    jugador que sera generado luego de comenzado el juego (estado in-game)
    """
    player = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, null = True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,
                            default='Default Name',
                            verbose_name='Planet name')
    seed = models.BigIntegerField(default=0, verbose_name='Planet seed')
    population_qty = models.IntegerField(default=5000,
                                         verbose_name='Population Amout',
                                         validators=[MinValueValidator(0)])
    missiles_qty = models.IntegerField(default=0,
                                       verbose_name='Missile Amount',
                                       validators=[MinValueValidator(0)])
    shield_perc = models.IntegerField(default=100,
                                      verbose_name='Shield Amount',
                                      validators=[MinValueValidator(0)])
    population_distr = models.IntegerField(default=100,
                                           verbose_name='Planet Population %',
                                           validators=[MinValueValidator(0)])
    shield_distr = models.IntegerField(default=0,
                                       verbose_name='Planet Shield %',
                                       validators=[MinValueValidator(0)])
    missile_distr = models.IntegerField(default=0,
                                        verbose_name='Planet Missile %',
                                        validators=[MinValueValidator(0)])

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
        new_planet = cls(player=player,
                         game=game,
                         name=name,
                         population_qty=game.initial_population,
                         seed=seed)
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

            self.save()
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
                self.shield_perc -= ammount
            else:
                self.shield_perc = 0
            self.save()
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
            self.population_qty -= ammount
        else:
            self.population_qty = 0

        self.save()

    def launch_missile(self, enemy_planet):
        """
        Launch missile:
        Crea un objeto Missile dirigido a un planeta objetivo
        INPUT: Objeto Planet, planeta enemigo
        OUTPUT: Bool que indica si pudo enviarse el misil
        """
        if (self.missiles_qty > 0):
            try:
                missile = Missile(owner=self, target=enemy_planet)
                missile.save()

                self.missiles_qty -= 1

                missile_launched = True
            except Missile.DoesNotExist:
                missile_launched = False
        else:
            missile_launched = False

        self.save()

        return missile_launched

    def get_missiles_state(self):
        """
        Get missiles state:
        Examina cada objeto Missile y obtiene el tiempo para impacto de cada
        uno
        INPUT: Objeto Planet
        OUTPUT: Diccionario con nombre de planetas y correspondientes tiempos
        de impacto
        """
        missiles = Missile.objects.all().filter(owner=self)
        times = {}

        for missile in missiles:
            times[missile.target.name] = missile.time_to_target()

        return times


class Defensive(Bot):
    """
    #Contiene informacion sobre los bot de caracteristica defensiva.
    """

    def attack(self):
        planet = PLanet.objects.get(bot = self)
        # Elegimos aleatoriamente el numero de misiles lanzados.
        count_attack = numpy.random.binomial(self.planet.missiles_qty,
                                             (self.probability_attack / 999.0))
        planets = Planet.objects.filter(game=self.game).exclude(
                                                               pk = planet,
                                                             population_qty = 0)
        # Seleccionamos aleatoriamente los planetas a atacar.
        planets_attack = numpy.random.poisson(1.5, count_attack)

        if not planets:
            for planet_id in planets_attack:
                if abs(planet_id) > (planets.count() - 1):
                    planet_id = planets.count() - 1
                self.planet.launch_missile(planets[abs(planet_id)])
                #print planets[abs(planet_id)]

    def defense(self):
        pass

class Offensive(Bot):
    """
    Representa al Bot ofensivo.
    """

    def attack(self):
        planet = Planet.objects.get(bot = self)
        planets=Planet.objects.filter(game=self.game).exclude(pk=planet,
                                                                population_qty=0);
        psorted=planets.sort(key=lambda x: x.shield_perc/x.population_qty)
        
        planets_to_attack=psorted[:planet.missiles_qty]
        if len(planets_to_attack) > 0:
            for p in planets_to_attack:
                planet.launch_missile(p)

    def change_distribution(self):
        planet = Planet.objects.get(bot = self)
        if planet.population_qty < 50:
            planet.assign_perc_rate(40, 10, 50)
        else:
            planet.assign_perc_rate(10, 10, 80)
        
            

class Alliance (models.Model):
    """
    Clase Alliance: Agrupa los planetas en alianzas si las hay en partida bajo un nombre.
    """
    name = models.CharField(max_length=30,default='Team',verbose_name='Alliance Name')
    game = models.ForeignKey(Game, default=1, on_delete=models.CASCADE,verbose_name='Game Name')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, game):
        """
        Create Alliance:
        Permite crear una alianza (equipo-team)
        INPUT: Partida donde vive la alianza
        OUTPUT: La Alianza
        """
        new_alliance = cls(name=name, game=game)
        return new_alliance


class Missile (models.Model):
    """
    Clase Missile: Contiene el planeta origen, planeta destino, y hora de
    lanzamiento
    """
    owner = models.ForeignKey(Planet, default=1, related_name="owner")
    target = models.ForeignKey(Planet, default=2, related_name="target")
    launch_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, owner, target):
        new_missile = cls(owner=owner, target=target)
        return new_missile

    def deal_damage(self):
        """
        Deal damage:
        Calcula el daño a escudo y poblacion del planeta enemigo
        INPUT: Objeto Missile
        OUTPUT: Ninguno
        """
        target = self.target
        gameroom = target.game

        damage_diminisher = (100.0 - float(self.target.shield_perc)) / 100.0
        damage = gameroom.hurt_to_population * damage_diminisher
        target.decrease_shield(gameroom.hurt_to_shield)
        target.decrease_population(damage)

        target.save()

    def time_to_target(self):
        """
        Time to target:
        Calcula el tiempo restante para el impacto
        INPUT: Objeto Missile
        OUTPUT: Tiempo para el impacto
        """
        gameroom = self.owner.game

        now = timezone.datetime.now(timezone.utc)
        missile_delay = timezone.timedelta(seconds=gameroom.time_missile)

        time_elapsed = self.launch_time - now
        time_to_impact = missile_delay - time_elapsed

        return time_to_impact
