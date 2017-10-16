# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Room(models.Model):
	"""
	Room Class: Contains all the information about a game lobby (pre-game status).
	"""
	creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Room Creator')
	room_name = models.CharField(max_length=20, verbose_name='Room Name')
	pub_date = models.DateTimeField(verbose_name='Date added')
	game_started = models.BooleanField(default=0,verbose_name='Game started (True/False)')
	max_players = models.IntegerField(default=0, verbose_name='Room players limit')
	connected_players = models.IntegerField(default=0, verbose_name='Amount of players online')
	bot_players = models.IntegerField(default=0, verbose_name='Amount of bot players')
	missile_delay = models.IntegerField(default=2, verbose_name='Missile Delay')
	init_population = models.IntegerField(default=0, verbose_name='Initial Population')
	const_population = models.IntegerField(default=1, verbose_name='Population Generation Constant')
	const_shield = models.IntegerField(default=1, verbose_name='Shield Generation Constant')
	const_missile = models.IntegerField(default=1, verbose_name='Missile Generation Constant')
	population_damage_per_missile = models.IntegerField(default=1, verbose_name='Population damage per missile')
	shield_damage_per_missile = models.IntegerField(default=1, verbose_name='Shield damage per missile')

	def __str__(self):
		return self.room_name

class Planet(models.Model):
	"""
	Planet Class: Contains all the information about each player's planet
	that will be generated after starting the game (in-game status).
	"""
	player = models.ForeignKey(User, on_delete=models.CASCADE)
	gameroom = models.ForeignKey(Room, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, null=False)
	seed = models.BigIntegerField(default=0)
	population_qty = models.IntegerField(default=0, verbose_name='Population Amout')
	missiles_qty = models.IntegerField(default=0, verbose_name='Missile Amount')
	shield_qty = models.IntegerField(default=0, verbose_name='Shield Amount')
	population_distr = models.IntegerField(default=100, verbose_name='Planet Population %')
	shield_distr = models.IntegerField(default=0, verbose_name='Planet Shield %')
  	missiles_distr = models.IntegerField(default=0, verbose_name='Planet Missile %')

	def __str__(self):
		return self.name

	@classmethod
  	def create(cls, player, gameroom, name, seed):
	    new_planet = cls(player=player,gameroom=gameroom,name=name,population_qty=gameroom.init_population,seed=seed)
	    return new_planet
