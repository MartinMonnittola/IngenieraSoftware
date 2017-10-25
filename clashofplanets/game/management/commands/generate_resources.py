from django.core.management.base import BaseCommand, CommandError
from game.models import *

class Command(BaseCommand):
    help = 'Generates the planet resources that belongs to an active room, everytime it gets executed.'

    def handle(self, *args, **options):
        active_games = Game.objects.filter(game_started=True)
        for g in active_games:
            planets_in_active_rooms = Planet.objects.filter(game=g)
            for p in planets_in_active_rooms:
                if p.population_qty < 5000:
                    p.population_qty += 1
                if p.shield_perc < 100:
                    p.shield_perc += 1
                p.missiles_qty += 1
                p.save()
        return "Planets have been refilled"
