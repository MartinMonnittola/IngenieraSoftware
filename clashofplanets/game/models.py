# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Room(models.Model):
	"""
	Room Class: Contains all the information about a game lobby (pre-game status).
	"""
	creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Room Creator')
	room_name = models.CharField(max_length=20, verbose_name='Room Name', default='Default Name')
	pub_date = models.DateTimeField(verbose_name='Date added')
	game_started = models.BooleanField(default=0,verbose_name='Game started (True/False)')
	max_players = models.IntegerField(default=0, verbose_name='Room players limit', blank=True, validators=[MinValueValidator(2)])
	connected_players = models.IntegerField(default=0, verbose_name='Amount of players online', validators=[MinValueValidator(0)])
	bot_players = models.IntegerField(default=2, verbose_name='Amount of bot players', validators=[MinValueValidator(2)])
	missile_delay = models.IntegerField(default=1, verbose_name='Missile Delay', validators=[MinValueValidator(1)])
	init_population = models.IntegerField(default=0, verbose_name='Initial Population', validators=[MinValueValidator(0)])
	const_population = models.IntegerField(default=1, verbose_name='Population Generation Constant', validators=[MinValueValidator(1)])
	const_shield = models.IntegerField(default=1, verbose_name='Shield Generation Constant', validators=[MinValueValidator(1)])
	const_missile = models.IntegerField(default=1, verbose_name='Missile Generation Constant', validators=[MinValueValidator(1)])
	population_damage_per_missile = models.IntegerField(default=1, verbose_name='Population damage per missile', validators=[MinValueValidator(1)])
	shield_damage_per_missile = models.IntegerField(default=1, verbose_name='Shield damage per missile', validators=[MinValueValidator(1)])

	def __str__(self):
		return self.room_name

class Planet(models.Model):
	"""
	Planet Class: Contains all the information about each player's planet
	that will be generated after starting the game (in-game status).
	"""
	player = models.ForeignKey(User, on_delete=models.CASCADE)
	gameroom = models.ForeignKey(Room, on_delete=models.CASCADE)
	name = models.CharField(max_length=20,verbose_name='Planet name')
	seed = models.BigIntegerField(default=0,verbose_name='Planet seed')
	population_qty = models.IntegerField(default=5000, verbose_name='Population Amout', validators=[MinValueValidator(0)])
	missiles_qty = models.IntegerField(default=0, verbose_name='Missile Amount', validators=[MinValueValidator(0)])
	shield_perc = models.IntegerField(default=0, verbose_name='Shield Amount', validators=[MinValueValidator(0)])
	population_distr = models.IntegerField(default=100, verbose_name='Planet Population %', validators=[MinValueValidator(0)])
	shield_distr = models.IntegerField(default=0, verbose_name='Planet Shield %', validators=[MinValueValidator(0)])
  	missile_distr = models.IntegerField(default=0, verbose_name='Planet Missile %', validators=[MinValueValidator(0)])

	def __str__(self):
		return self.name

	@classmethod
  	def create(cls, player, gameroom, name, seed):
	    new_planet = cls(player=player,gameroom=gameroom,name=name,population_qty=gameroom.init_population,seed=seed)
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
