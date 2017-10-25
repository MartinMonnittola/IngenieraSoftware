# Synergia

## Preparacion del entorno virtual:

	virtualenv NOMBRE
	source NOMBRE/bin/activate
	pip install -r requirements.txt

## Ejecucion:

	python manage.py makemigrations game
	python manage.py migrate game
    python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

## Comentario General del proyecto:

	Lo que se logro hasta el momento:
		Registro, login, logout, instrucciones del juego.
		Crear, listar, unirse, y abandonar partidas.
        	Mecanica del juego: Atacar planetas enemigos, asignar una distribucion de poblacion para generar recursos, battleLog de la 		   partida.
        	Estetica del juego: Si bien en algun momento se piensa implementar un canvas que haga mas dinamico e interactivo al juego,
        	por el momento se implemento un estilo moderno futurista que va con el mismo.

	Fuentes:
		Stackoverflow
       		Manual Django 1.11
        	Referencias de otros proyectos de mecanica similar (Mafia Wars, Space Battle, Mob Wars)
