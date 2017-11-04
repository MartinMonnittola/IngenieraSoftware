# Synergia

## Requerimientos ##

* Python3
* Django 1.11
* Bash

## Instrucciones para correr el juego ##

1. Clonar el repositorio: git clone https://github.com/ingsoft-famaf/synergia.git
2. cd synergia/clashofplanets
3. python manage.py makemigrations game
4. python manage.py migrate game
5. python manage.py makemigrations
6. python manage.py migrate
7. ./start.sh

## Uso de start.sh ##

Usage: ./start.sh [-l IP:PORT] [-u SECONDS] [-h]

Al ejecutar este comando el juego debe arrancar correctamente, se puede verificar ingresando desde el navador a la dirección http://127.0.0.1:8000
Si no se especifican los argumentos, el juego se ejecutará escuchando en 127.0.0.1:8000 y con un intérvalo de actualización de 2 segundos. No se debe ejecutar el comando runserver de Django directamente, siempre el juego debe llamarse desde start.sh.

## Demo Online ##
El juego se puede probar online en la siguiente dirección:
    https://synergiacop.heroku.com

