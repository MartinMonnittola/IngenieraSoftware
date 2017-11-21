from django.core.management.base import BaseCommand, CommandError
from game.models import *

class Command(BaseCommand):
    help = 'Generates the planet resources that belongs to an active room, everytime it gets executed.'

    def handle(self, *args, **options):
        active_games = Game.objects.filter(game_started=True, game_finished=False)
        for g in active_games:
            planets_in_active_rooms = Planet.objects.filter(game=g)
            if g.num_alliances < 2:
                planets_alive_in_game = Planet.objects.filter(game=g,is_alive=True).count() # planets alive in game
                if planets_alive_in_game == 1:
                    g.game_finished = True
            else:
                alliances_in_game = Alliance.objects.filter(game=g)
                for alliance in alliances_in_game:
                    planets_alive_in_alliance = Planet.objects.filter(game=g, alliance=alliance, is_alive=True).count()
                    if planets_alive_in_alliance >= 1:
                        alliance.is_winner = True
                    else:
                        alliance.is_winner = False
                    alliance.save()
                alliance_winner = Alliance.objects.filter(game=g,is_winner=True).count()
                if alliance_winner == 1:
                    g.game_finished = True
            g.save()
            for p in planets_in_active_rooms:
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

            if (g.bot_def_num) > 0:
                bots_def = Defensive.objects.filter(game = g)
                for bot in bots_def:
                    planet = Planet.objects.get(bot = bot)
                    print planet, g
                    if planet.population_qty > 0:
                        bot.attack()
                        #print "Estamos cambiando la distribucion."
                        bot.change_distribution()
                        #print "Estamos enviando poblacion."
                        bot.send_population()

            if (g.bot_ofc_num) > 0:
                bots_ofc = Offensive.objects.filter(game = g)
                for bot in bots_ofc:
                    planet = Planet.objects.get(bot = bot)
                    if planet.population_qty > 0:
                        bot.attack()
                        #print "Estamos cambiando la distribucion."
                        bot.change_distribution()
                        #print "Estamos enviando poblacion."
                        bot.send_population()

        return "Command Generate Executed"
