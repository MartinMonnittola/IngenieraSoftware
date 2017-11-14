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
                    if p.population_qty + calculo_generar_pop > 10000:
                        p.population_qty = 10000
                    else:
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
                p.save()
                ##### MISSILES ####
                missiles_from_planet = Missile.objects.filter(owner=p,is_active=True)
                for m in missiles_from_planet:
                    m_2_t = m.time_to_target()
                    if m_2_t.total_seconds() <= 0:
                        m.deal_damage()

        return "Planets have been refilled"
