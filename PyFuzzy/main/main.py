# -*- coding: utf-8 -*-
## Importation des bibliotheques
# Gestion du temps
import time
# Communiquer avec les composants du robots
from ev3dev.ev3 import *
# Interpreteur et calculateur de logique floue
import fuzzy.storage.fcl.Reader as fclRead

## Definitions des objets
# Fichier des lois de fuzzification
system = fclRead.Reader().load_from_file("def.FCL")
# Moteurs de l'EV3
FrontRight = LargeMotor('outA')
FrontLeft = LargeMotor('outD')
BackRight = LargeMotor('outB')
BackLeft = LargeMotor('outC')
# Capteur de l'EV3
captUS = UltrasonicSensor(INPUT_1)
captUS.mode = 'US-DIST-CM'
# Fichier de monitoring
data = open("data.csv","w")

## Variables
# Variables du programme
# Tableau des distances
d=[]
# Initialisation de la vitesse (vitesse maximale) en deg/s
speed = 300
# Temps entre deux prises de valeurs de distance
dt=0.1
# Initialisation du pas de temps
begin=0
end=0.1

## Fonctions de variations de vitesse
# Acceleration
def acc(speed) :
	if speed < 150 :
		coef = speed/299 + 149/299
	elif speed >= 150 :
		coef = speed/150
	up_sp = 4/3 - (2/3)*coef
	return(speed + speed*up_sp)
# Desceleration
def desc(command_speed,speed) :
	dw_sp = 1 - command_speed/2
	speed = speed - dw_sp*speed
	if speed < 100:
		speed = 100
	return(speed)
# Freinage
def freiner(command_speed,speed):
	dw_sp = 2 - command_speed
	return(speed - dw_sp*speed)

# Variables fuzzy
inputs = {
 "given_speed" : 0.0,
 "obstacle_speed" : 0.0,
 "distance" : 0.0
 }
output = {
 "command_speed" : 0.0
 }

## Programme principal
# Initialisation du tableau des distances a l'obstacle
for i in range(3):
	# Distance a l'obstacle en mm
	distance=captUS.value()
	d.append(distance)
	# Prise des valeurs a dt secondes d'intervalle
	time.sleep(dt)
# Initialisation du chronometre global pour le monitoring
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

	## Creation du tableau des vitesses de l'obstacle
	T = []
	distance = captUS.value()
	d.append(distance)
	for i in range(3):
		# Calcul de la vitesse de l'obstacle par rapport au vehicule en mm/s
		v = (d[i+1]-d[i]) / dt
		T += [v]
	# Calcul de la vitesse moyenne de l'obstacle
	VobsMoy = (T[0]+T[1]+T[2])/3

	## Insertions des valeurs a fuzzyfier
	inputs["given_speed"] = speed
	inputs["obstacle_speed"] = VobsMoy
	inputs["distance"] = distance
	# Fuzzyfication
	system.calculate(inputs, output)
	# Recuperation de la resultante des regles de defuzzyfication
	command_speed = output["command_speed"]

	## Reactions du vehicule
	# Methode d'interruption : rompt la boucle et effectue la fin du programme
	if distance <= 50 :
		FrontRight.stop()
		FrontLeft.stop()
		BackRight.stop()
		BackLeft.stop()
		break
	# Conditions sur l'acceleration
	if command_speed > 2 :
		speed = acc(speed)
	# Conditions sur la desceleration
	elif command_speed <= 1.1 :
		speed = 0.5
	elif command_speed < 2 and command_speed >= 1.5 :
		speed = desc(command_speed,speed)
	elif command_speed < 1.5 and command_speed >= 1:
		speed = freiner(command_speed, speed)
	# Limitation de la vitesse
	if speed > 300:
		speed = 300.
	elif speed < 0.5:
		speed = 0.5

	# Calcul du temps ecoule depuis l'initialisation
	temps = time.time() - init
	# Insertion des donnees a monitorer dans le fichier
	data.write("%f/%f/%d/%f/%f\n" % (temps, command_speed, distance, speed, VobsMoy))

	## Fin de la boucle
	# Suppression de la premiere valeur du tableau des distances
	del d[0]
	# Recuperation du temps en fin de boucle pour determiner dt
	end = time.time()

## Fin du programme
# Fermeture du fichier de monitoring
data.close()
# Signalisation de la fin du programme
Leds.set_color(Leds.LEFT, Leds.GREEN)
Leds.set_color(Leds.RIGHT, Leds.GREEN)