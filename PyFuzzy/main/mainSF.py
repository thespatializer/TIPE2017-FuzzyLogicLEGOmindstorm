# -*- coding: utf-8 -*-
## Importation des bibliotheques
# Gestion du temps
import time
# Communiquer avec les composants du robots
from ev3dev.ev3 import *

## Definitions des objets
# Moteurs de l'EV3
FrontRight = LargeMotor('outA')
FrontLeft = LargeMotor('outD')
BackRight = LargeMotor('outB')
BackLeft = LargeMotor('outC')
# Capteur de l'EV3
captUS = UltrasonicSensor(INPUT_1)
captUS.mode = 'US-DIST-CM'
# Fichier de monitoring
data = open("dataSF.csv", "w")

## Variables
# Tableau des distances
d = []
# Initialisation de la vitesse (vitesse maximale) en deg/s
speed = 300
# Temps entre deux prises de valeurs de distance
dt = 0.1
# Initialisation du pas de temps en secondes
begin = 0
end = 0.1
# Distance de securite en mm a maintenir avec l'obstacle
DistSecure = 500

## Fonctions de variations de vitesse
# Acceleration
def acc(speed) :
	if speed < 150 :
		coef = speed/299 + 149/299
	elif speed >= 150 :
		coef = speed / 150
	up_sp = 4/3 - (2/3)*coef
	return(speed + speed*up_sp)
# Freinage
def freiner(speed) :
	if speed > 150 :
		speed = 150
	elif speed <= 150 :
		dw_sp = 0.1
		speed = speed - dw_sp*speed
	return(speed)

## Programme principal
# Initialisation du tableau des distances a l'obstacle
for i in range(3):
	# Distance a l'obstacle en mm
	distance=captUS.value()
	d.append(distance)
	# Prise des valeurs a dt secondes d'intervalle
	time.sleep(dt)
# Initialisation du chrono global pour le monitoring
init = time.time()
# Utilisation des LEDs pour indiquer que la boucle commence
Leds.set_color(Leds.LEFT, Leds.YELLOW)
Leds.set_color(Leds.RIGHT, Leds.YELLOW)

## Boucle du programme
while True :
	# Determination de la duree d'une boucle
	dt = end - begin
	begin = time.time()

	# Modification de la vitesse
	FrontRight.speed_sp = speed
	FrontLeft.speed_sp = speed
	BackRight.speed_sp = -speed
	BackLeft.speed_sp = -speed
	FrontRight.run_forever()
	FrontLeft.run_forever()
	BackRight.run_forever()
	BackLeft.run_forever()

	## Creation du teableau des vitesses de l'obstacle
	T = []
	distance = captUS.value()
	d.append(distance)
	for i in range(3) :
		# Calcule de la vitesse de l'obstacle par rapport au vehicule en mm/s
		v = (d[i+1]-d[i]) / dt
		T += [v]
	# Calcul de la sortie et recuperation de la moyenne globale
	VobsMoy = (T[0]+T[1]+T[2]) / 3

	## Reactions du vehicule
	# Methode d'interruption : rompte la boucle et effectue la fin du programme
	if distance <= 50 :
		FrontRight.stop()
		FrontLeft.stop()
		BackRight.stop()
		BackLeft.stop()
		break
	# Conditions sur l'acceleration
	if VobsMoy >= 0 and distance > DistSecure :
		speed = acc(speed)
	# Conditions sur la desceleration
	elif VobsMoy < 0 and distance < DistSecure :
		speed = freiner(speed)
	# Limitation de la vitesse
	if speed > 300:
		speed = 300.
	elif speed < 0.5:
		speed = 0.5
	# Calcul du temps ecoule depuis l'initialisation
	temps = time.time() - init
	# Insertion des donnees a monitorer dans le fichier
	data.write("%f/%f/%d/%f/%f\n" % (temps, distance, speed, VobsMoy))

	## Fin de la boucle
	# Suppression de la premiere valeur du tableau des distances
	del d[0]
	end = time.time()

## Fin du programme
# Fermeture du fichier de monitoring
data.close()
# Signalisation de la fin du programme
Leds.set_color(Leds.LEFT, Leds.GREEN)
Leds.set_color(Leds.RIGHT, Leds.GREEN)