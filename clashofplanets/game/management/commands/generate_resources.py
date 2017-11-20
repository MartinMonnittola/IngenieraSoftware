from django.core.management.base import BaseCommand, CommandError
from game.models import *

class Command(BaseCommand):
    help = 'Generates the planet resources that belongs to an active room, everytime it gets executed.'

    def handle(self, *args, **options):
        active_games = Game.objects.filter(game_started=True)
        for g in active_games:
            planets_in_active_rooms = Planet.objects.filter(game=g)
            for p in planets_in_active_rooms:
                if p.population_qty < 10000:
                    cantidad_asig = p.population_qty * p.population_distr / 100
                    calculo_generar_pop = cantidad_asig / g.const_population
                    p.population_qty += calculo_generar_pop
                if p.shield_perc < 100:
                    cant_asig_shield = p.population_qty * p.shield_distr / 100
                    calculo_generar_shield = cant_asig_shield / g.const_shield
                    if (p.shield_perc + calculo_generar_shield) > 100:
                        p.shield_perc = 100
                    else:
                        p.shield_perc += calculo_generar_shield
                cant_asig_mis = p.population_qty * p.missile_distr / 100
                calculo_generar_missile = cant_asig_mis / g.const_missile
                p.missiles_qty += calculo_generar_missile
                if p.population_qty < 1:
                    p.is_alive = False
                p.save()

            if g.bot_players > 0:
                bots = Defensive.objects.filter(game = g)
                if bots is None:
                    bots = Offensive.objects.filter(game = g)

                for bot in bots:
                    planet = Planet.objects.get(bot = bot)
                    if planet.population_qty > 0:
                        bot.attack()
                        print "Estamos cambiando la distribucion."
                        bot.change_distribution()
                        print "Estamos enviando poblacion."
                        bot.send_population()
        return "Planets have been refilled"
