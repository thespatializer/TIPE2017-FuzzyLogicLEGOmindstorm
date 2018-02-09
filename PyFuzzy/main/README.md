# main
This directory contains two Python 3.6 scripts, one Fuzzy Control Language file and two CSV files used for getting data and making nice graphs.
__They need to be in the same directory in order to work__

# main.py
This is the program used to control the speed prototype using fuzzy logic.
Inputs are the distance from the obstacle and the actual speed of rotation of the 4 motors.
Inputs transfered to the FL algorithm are the distance, the speed and an approximated notion of the obstacle's speed (calculated in the program).
Output of the FL algorithm is a value named command_speed included in {0}U[1;3] which is then interprated by the program in order to influence on the speed of rotation of the 4 motors.
Output is the speed of the vehicule.
The program automatically shuts itself when an obstacle is detected under 5cm.

# mainSF.py
This is the programe used to prove FL is cool as it does the same things as main.py but does not implement PyFuzzy.
Inputs are the distance from the obstacle and the speed of rotation of the 4 motors.
Output is the speed of the vehicle.

# def.FCL
This is the file that describes the rules for fuzzyfying inputs and defuzzyfying the results. It follows the Fuzzy Control Language norme and is interpreted by ANTLR3 implemented by PyFuzzy.
It is divided in 4 parts :
1. Variables definition (Inputs and Outputs)
2. Fuzzy terms definition
3. Defuzzyfying terms and method
4. Fuzzy rules

# data.csv
Monitoring file for main.py
Each line indicates instantaneous values of:
* temps : time passed in s from the beginning of the program
* command_speed : deffuzyfied value
* distance : obvious
* speed : obvious
* VobsMoy : obstacle's average speed
Each of these values are separated from the others by a "/" which can be used as column separator in a spreadsheet.

# dataSF.csv
Monitoring file from mainSF.py
Each line indicates instantaneous values of:
* temps : time passed in s from the beginning of the program
* distance : obvious
* speed : obvious
* VobsMoy : obstacle's average speed
Each of these values are separated from the others by a "/" which can be used as column separator in a spreadsheet.