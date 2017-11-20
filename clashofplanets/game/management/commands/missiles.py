from django.core.management.base import BaseCommand, CommandError
from game.models import *

class Command(BaseCommand):
    help = 'Check and deal damage of active missiles.'

    def handle(self, *args, **options):
        active_games = Game.objects.filter(game_started=True)
        for g in active_games:
            planets_in_active_rooms = Planet.objects.filter(game=g)
            for p in planets_in_active_rooms:
                ##### MISSILES #####
                missiles_from_planet = Missile.objects.filter(owner=p,is_active=True)
                for m in missiles_from_planet:
                    print "hols"
                    m_2_t = m.time_to_target()
                    if m_2_t.total_seconds() <= 0:
                        m.deal_damage()
        return "Missiles have been checked"
