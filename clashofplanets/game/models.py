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
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Game user')
    # Nombre de la partida.
    game_name = models.CharField(max_length=20, verbose_name='Game Name',default='Default Name')
    # Tiempo en el que se inicio la partida.
    pub_date = models.DateTimeField(verbose_name='Date added',default=timezone.now)
    # Estado de la partida.
    game_started = models.BooleanField(default=0, verbose_name='Game started (True/False)')
    # Juego finalizado
    game_finished = models.BooleanField(default=0, verbose_name='Game Finished (True/False)')
    # Numero de alianzas
    num_alliances = models.IntegerField(default=1, verbose_name='Number of Alliances', blank=True, validators=[MinValueValidator(0)])
    # Numero maximo de jugadores.
    max_players = models.IntegerField(default=0, verbose_name='Game players limit', blank=True, validators=[MinValueValidator(2)])
    # Numero de jugadores que se unieron a la partida.
    connected_players = models.IntegerField(default=0, verbose_name='Connected players', validators=[MinValueValidator(0)])
    # Numero de bots defensivos que se agregaron a la partida a la partida.
    bot_def_num = models.IntegerField(default=0, verbose_name='Amount of bot players (DEF)', validators=[MinValueValidator(0)])
    # Numero de bots defensivos que se agregaron a la partida a la partida.
    bot_ofc_num = models.IntegerField(default=0, verbose_name='Amount of bot players (OFC)', validators=[MinValueValidator(0)])
    # Tiempo de viaje del misil.
    time_missile = models.IntegerField(default=10, verbose_name='Missile Delay', validators=[MinValueValidator(1)])
    # Poblacion inicial al comenzar la partida.
    initial_population = models.IntegerField(default=1000, verbose_name='Initial Population', validators=[MinValueValidator(0)])
    # Procentaje de poblacion asignado al recurso poblacion.
    const_population = models.IntegerField(default=400, verbose_name='Population Genration Constant', validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso escudo.
    const_shield = models.IntegerField(default=500, verbose_name='Shield Generation Constant', validators=[MinValueValidator(1)])
    # Procentaje de poblacion asignado al recurso misil.
    const_missile = models.IntegerField(default=700, verbose_name='Missile Generation Constant', validators=[MinValueValidator(1)])
    # DaÃ±o a la poblacion por misil.
    hurt_to_population = models.IntegerField(default=100, verbose_name='Population damage per missile', validators=[MinValueValidator(1)])
    # DaÃ±o a la escudo por misil.
    hurt_to_shield = models.IntegerField(default=10, verbose_name='Shield damage per missile', validators=[MinValueValidator(1)])
    FAST = 1
    SLOW = 2
    MODE_CHOICES = (
        (FAST, 'Fast'),
        (SLOW, 'Slow')
    )
    FAST_CONSTANTS = {
        'time_missile': 1,
        'initial_population': 1000,
        'const_missile': 900,
        'const_population': 25,
        'const_shield': 1500,
        'hurt_to_population': 500,
        'hurt_to_shield': 20
    }
    SLOW_CONSTANTS = {
        'time_missile': 10,
        'initial_population': 1000,
        'const_missile': 700,
        'const_population': 500,
        'const_shield': 300,
        'hurt_to_population': 100,
        'hurt_to_shield': 10
    }
    mode = models.CharField(
        max_length=1,
        choices=MODE_CHOICES,
        default=FAST,
    )

    def __str__(self):
        """
        Retorna la representacion del objeto en forma de string.
        """
        return self.game_name

    @classmethod
    def create(cls, owner, name, max_players, num_alliances, mode, bot_def, bot_ofc):
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
                   bot_def_num=bot_def,
                   bot_ofc_num=bot_ofc,
                   user=owner,
                   num_alliances=num_alliances)
        game.configure_mode(mode)
        return game

    def configure_mode(self, mode):
        if mode == self.FAST:
            self.mode = self.FAST
            self.time_missile = self.FAST_CONSTANTS['time_missile']
            self.initial_population = self.FAST_CONSTANTS['initial_population']
            self.const_missile = self.FAST_CONSTANTS['const_missile']
            self.const_population = self.FAST_CONSTANTS['const_population']
            self.const_shield = self.FAST_CONSTANTS['const_shield']
            self.hurt_to_population = self.FAST_CONSTANTS['hurt_to_population']
            self.hurt_to_shield = self.FAST_CONSTANTS['hurt_to_shield']
        elif mode == self.SLOW:
            self.mode = self.SLOW
            self.time_missile = self.SLOW_CONSTANTS['time_missile']
            self.initial_population = self.SLOW_CONSTANTS['initial_population']
            self.const_missile = self.SLOW_CONSTANTS['const_missile']
            self.const_population = self.SLOW_CONSTANTS['const_population']
            self.const_shield = self.SLOW_CONSTANTS['const_shield']
            self.hurt_to_population = self.SLOW_CONSTANTS['hurt_to_population']
            self.hurt_to_shield = self.SLOW_CONSTANTS['hurt_to_shield']
        else:
            raise NameError('Wrong Mode')

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
                alliances = Alliance.objects.all().filter(game = self).order_by('num_players')
                alliance = alliances.first()

                planet = Planet.create(player = user, bot = None, game = self,
                                       name = name, seed = seed,
                                       alliance = alliance)
                planet.save()

                alliance.add_player()
                alliance.save()

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


class Alliance (models.Model):
    """
    Clase Alliance: Agrupa los planetas en alianzas si las hay en partida bajo
    un nombre.
    """
    name = models.CharField(max_length=30, default='Team', verbose_name='Alliance Name')
    game = models.ForeignKey(Game, default=1, on_delete=models.CASCADE, verbose_name='Game Name')
    num_players = models.IntegerField(default=0, verbose_name='Players Quantity')
    is_winner = models.BooleanField(default=False, verbose_name='Winner Of Game')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, game):
        """
        Create Alliance:
        Permite crear una alianza (equipo-team)
        INPUT: Nombre de la alianza, partida a la que pertenece
        OUTPUT: La alianza
        """
        new_alliance = cls(name=name, game=game)
        return new_alliance

    def add_player(self):
        """
        Add Player:
        Aumenta el contador de jugadores pertenecientes a la alianza
        INPUT: Ninguno
        OUTPUT: Ninguno
        """
        self.num_players += 1
        self.save()

    def remove_player(self):
        """
        Add Player:
        Decrementa el contador de jugadores pertenecientes a la alianza
        INPUT: Ninguno
        OUTPUT: Ninguno
        """
        self.num_players -= 1
        self.save()


class Bot(models.Model):
    """
    Clase abstracta que representa a los bot.
    """
    # Probabilidad de decidir atacar.
    probability_attack = models.IntegerField(default=99, help_text='probability of attack', blank=False)

    # Probabilidad de decidir modificar los recursos.
    probability_modify_resources = models.IntegerField(default=60, help_text='probability of modifying resources', blank=False)
    # Probabilidad de enviar poblacion a otro planeta.
    probability_send_population = models.IntegerField(default=60, help_text='probability of send population', blank=False)
    # Partida a la que pertenece el bot.
    game = models.ForeignKey(Game, default = 1, on_delete = models.CASCADE)
    # Nombre del bot.
    name = models.CharField(max_length=20, blank=False, verbose_name='Bot name')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, game):
        """
        Permite crear un bot.
        Entrada: Game, la partida a la que pertenece.
        Salida: objeto Bot.
        """
        try:
            max_pk = Bot.objects.all().order_by("-pk").first().pk
            max_pk = max_pk + 1
        except:
            max_pk = 1
        bot = cls(name = ('Bot'+ str(max_pk)), game=game,
                          probability_attack = 30,
                          probability_modify_resources = 60,
                          probability_send_population = 60
                         )
        bot.save()
        return bot

    def attack(self):
        """
        Decide aleatoriamente si ataca a uno o mas planetas.
        """
        pass

    def change_distribution(self):
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
    alliance = models.ForeignKey(Alliance, default = 1, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='Default Name', verbose_name='Planet name')
    is_alive = models.BooleanField(default=True, verbose_name='Planet Alive')
    seed = models.BigIntegerField(default=0, verbose_name='Planet seed')
    population_qty = models.IntegerField(default=5000, verbose_name='Population Amout', validators=[MinValueValidator(0)])
    missiles_qty = models.IntegerField(default=0, verbose_name='Missile Amount', validators=[MinValueValidator(0)])
    shield_perc = models.IntegerField(default=100, verbose_name='Shield Amount', validators=[MinValueValidator(0)])
    population_distr = models.IntegerField(default=100, verbose_name='Planet Population %', validators=[MinValueValidator(0)])
    shield_distr = models.IntegerField(default=0, verbose_name='Planet Shield %', validators=[MinValueValidator(0)])
    missile_distr = models.IntegerField(default=0, verbose_name='Planet Missile %', validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, player, bot, game, name, seed, alliance):
        """
        Create Planet:
        Permite a los jugadores crear sus planetas
        INPUT: DueÃ±o del planeta, partida a la que pertenece,
               nombre del planeta y un seed al azar
        OUTPUT: Objeto Planet
        """
        new_planet = cls(player=player,
                         game=game,
                         bot=bot,
                         name=name,
                         population_qty=game.initial_population,
                         seed=seed,
                         alliance=alliance,)
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
        INPUT: Objeto Planet, cantidad de daÃ±o
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
        INPUT: Objeto Planet, cantidad de daÃ±o
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

    def send_population(self, target_planet):
        """
        Send population:
        Envia poblaciona a un planeta
        INPUT: Objetos Planet de origen (self) y destino (target_planet)
        OUTPUT: Mensaje indicando exito (1) o fallo (0)
        """
        if self.population_qty > 100 and target_planet.population_qty > 1:
            self.population_qty -= 100
            self.save()
            target_planet.population_qty += 100
            target_planet.save()
            send_pop_message = 1
        else:
            send_pop_message = 0
        return send_pop_message


class Defensive(Bot):
    """
    Contiene informacion sobre los bot de caracteristica defensiva.
    """
    def attack(self):
        planet = Planet.objects.get(bot = self)
        # Elegimos aleatoriamente el numero de misiles lanzados.
        count_attack = numpy.random.binomial(planet.missiles_qty,
                                             (self.probability_attack/51.0))
        planets_game = Planet.objects.filter(game=self.game).exclude(bot = self)
        planets_alive = planets_game.exclude(is_alive=False)
        if 2 <= self.game.num_alliances:
            planets_rival = planets_alive.exclude(alliance = planet.alliance)
        else:
            planets_rival = planets_alive

        # Ordenamos los planetas a atacar segun su poblacion y escudo en orden
        # creciente.

        planets = planets_rival.order_by('population_qty', 'shield_perc')
        # Seleccionamos aleatoriamente los planetas a atacar.
        planets_attack = numpy.random.poisson(1.5, count_attack)
        if not (planets is None):
            for planet_id in planets_attack:
                if abs(planet_id) > (planets.count() - 1):
                    planet_id = planets.count() - 1
                planet.launch_missile(planets[abs(planet_id)])
                planets[abs(planet_id)].save()

    def change_distribution(self):
        # Obtenemos la cantidad de habitantes del planeta mas poblado.
        planets = Planet.objects.filter(game=self.game).exclude(bot = self)
        planet_max = planets.order_by('-population_qty').first()
        # Calculamos la cantidad maxima de poblacion que se tomara como
        # referencia.
        max_popult = planet_max.population_qty + planet_max.population_qty * 0.6
        # Calculamos la nueva distribucion de cada atributo.
        planet = Planet.objects.get(bot = self)
        if planet.population_qty < max_popult :
            media =  100 * (1 - (planet.population_qty / max_popult))
            std_dev = planet.population_qty / max_popult
        else:
            media = 0.000001
            std_dev = 0.000001
        population_distr = numpy.random.normal(media, std_dev)
        if population_distr > 100:
            population_distr = 100
        if population_distr < 0:
            population_distr = 0
        media = (100 - population_distr) * 0.7
        std_dev = 0.8
        shield_distr = numpy.random.normal(media, std_dev)
        if shield_distr > (100 - population_distr):
            population_distr = (100 - population_distr)
        if shield_distr < 0:
            shield_distr = 0
        missile_distr = 100 - (shield_distr + population_distr)
        planet.assign_perc_rate(population_distr, shield_distr, missile_distr)
        planet.save()


    def send_population(self):
        planet = Planet.objects.get(bot = self)
        # Obtenemos la cantidad de habitantes del planeta mas poblado.
        planets_popult = Planet.objects.filter(game=self.game)
        planet_max = planets_popult.order_by('-population_qty').first()
        # Calculamos la cantidad maxima de poblacion que se tomara como
        # referencia para estimar la pobabiidad de enviar pobladores.
        max_popult = planet_max.population_qty
        probability_send_population = ((planet.population_qty / max_popult) * self.probability_send_population)
        planets_game = Planet.objects.filter(game=self.game).exclude(bot = self)
        planets_friends = planets_game.filter(alliance = planet.alliance)
        planets = planets_friends.exclude(population_qty = 0).order_by('population_qty')
        count_send = numpy.random.binomial(planets.count(),(probability_send_population/ 999.0))
        planets_sends = numpy.random.poisson(1.5, count_send)
        if not (planets is None):
            for planet_id in planets_sends:
                if abs(planet_id) > (planets.count() - 1):
                    planet_id = planets.count() - 1
                planet.send_population(planets[abs(planet_id)])


class Offensive(Bot):
    """
    Representa al Bot ofensivo.
    """

    def attack(self):
        planet = Planet.objects.get(bot = self)
        game_in = Game.objects.get(pk=planet.game.id)
        if game_in.num_alliances < 2:
            planets=Planet.objects.filter(game=self.game, is_alive=True).exclude(bot=self)
        else:
            planets=Planet.objects.filter(game=self.game, is_alive=True).exclude(bot=self, alliance=planet.alliance)
        psorted=planets.order_by('shield_perc','population_qty')
        planets_to_attack=psorted[:planet.missiles_qty]
        if len(planets_to_attack) > 0:
            for p in planets_to_attack:
                planet.launch_missile(p)

    def change_distribution(self):
        planet = Planet.objects.get(bot = self)
        game_in = Game.objects.get(pk=planet.game.id)
        game_cm = game_in.const_missile
        game_cp = game_in.const_population
        if planet.population_qty < game_cm and planet.shield_perc > 50:
            planet.assign_perc_rate(100, 0, 0)
        elif planet.population_qty > game_cm and planet.missiles_qty == 0:
            planet.assign_perc_rate(10, 0, 90)
        elif planet.shield_perc <= 50:
            planet.assign_perc_rate(20, 70, 10)
        else:
            planet.assign_perc_rate(20, 10, 70)

    def send_population(self):
        planet = Planet.objects.get(bot = self)
        planets=Planet.objects.filter(game=self.game, is_alive=True, alliance=planet.alliance).exclude(pk=planet.id)
        psorted=planets.order_by('shield_perc','population_qty')
        game_in = Game.objects.get(pk=planet.game.id)
        game_cm = game_in.const_missile
        game_cp = game_in.const_population
        planets_to_send=psorted[:planet.population_qty]
        if len(planets_to_send) > 0:
            for p in planets_to_send:
                if (planet.population_qty > (game_cm+100) and (p.population_qty < game_cp/2)):
                    planet.send_population(p)


class Missile (models.Model):
    """
    Clase Missile: Contiene el planeta origen, planeta destino, y hora de
    lanzamiento
    """
    owner = models.ForeignKey(Planet, default=1, related_name="owner")
    target = models.ForeignKey(Planet, default=2, related_name="target")
    launch_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, owner, target):
        new_missile = cls(owner=owner, target=target)
        return new_missile

    def deal_damage(self):
        """
        Deal damage:
        Calcula el daÃ±o a escudo y poblacion del planeta enemigo
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

        self.is_active = False
        self.save()

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

        time_elapsed = now - self.launch_time
        time_to_impact = missile_delay - time_elapsed

        return time_to_impact
