import RPi.GPIO as GPIO
import pigpio #Run this command everytime: sudo apt-get install python3-pigpio; sudo pigpiod
import time
import math
from flask import flash

#Portas para os PWM de cada Servo
servo_H = 17
servo_V = 18

#Constantes da Câmera (Informacao no datasheet) https://www.raspberrypi.com/documentation/accessories/camera.html
f=3.04; #Distancia focal da Câmera [em mm]; 
Sx=(1.12*10^-3); # Constante de transformação entre pixel para mm;

#Limites de Rotação [em graus] https://www.datasheet4u.com/datasheet-pdf/TowerPro/SG90/pdf.php?id=791970
#Deve-se alterar esses limites quando for testado no Tilt (percebi esse problema com o pessoal da outra equipe)
max_H=90;
max_V=90;
min_H=-90;
min_H=-90;


# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi() #Inicia biblioteca

#Define os Servos com Output
pwm.set_mode(servo_H, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_H, 50 )
pwm.set_mode(servo_V, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_V, 50 )


def toggle_servo(X):#1-Servo ON; 0 - Servo OFF
    if (X):
        pwm.set_mode(servo_H, pigpio.OUTPUT)
        pwm.set_PWM_frequency( servo_H, 50 )
        pwm.set_mode(servo_V, pigpio.OUTPUT)
        pwm.set_PWM_frequency( servo_V, 50 )
    else:
        pwm.set_PWM_dutycycle(servo_H, 0)
        pwm.set_PWM_frequency(servo_H, 0)
        pwm.set_PWM_dutycycle(servo_V, 0)
        pwm.set_PWM_frequency(servo_V, 0)
        flash('Servos OFF');

def func(x): #Retorna o valor em segundos [para o t_{on} do PWM] da rotacao em graus desejada
    return ((90-(-90))/(2000-1000))*x+1500 #Funcao de primeiro grau

def inv_func(y): #Retorna o valor em graus de um dutycycle em segundos
    return (50*y-75000)/9 #https://pt.symbolab.com/solver/function-inverse-calculator/inversa%20f%5Cleft(x%5Cright)%3D%5Cleft(%5Cleft(90-%5Cleft(-90%5Cright)%5Cright)%2F%5Cleft(2000-1000%5Cright)%5Cright)%5Ccdot%20x%2B1500?or=input

def checa_angulo(angulo_V=0,angulo_H=0):#Retorna 0 se estiver errado e flash o periodo correto dos angulos; Retorna 1 se correto;
    #me pergunto o que aconteceria com o flash() se enviasse os dois angulos errados
    if (float(angulo_H)<min_H or float(angulo_H)>max_H) or (float(angulo_V)<min_V or float(angulo_V)>max_V):
        
        if (float(angulo_H)<min_H or float(angulo_H)>max_H):
            if (float(angulo_H)<min_H):
                pwm.set_servo_pulsewidth( servo_H, func(min_H));
            elif (float(angulo_H)>max_H):
                pwm.set_servo_pulsewidth( servo_H, func(max_H));
        
        message="ERROR: Angulo Horizontal fora de faixa ["+str(min_H)+","+str(max_H)+"]"
        flash(message)
        
        if (float(angulo_V)<min_V or float(angulo_V)>max_V):
            if (float(angulo_V)<min_v):
                pwm.set_servo_pulsewidth( servo_V, func(min_V));
            elif (float(angulo_V)>max_V):
                pwm.set_servo_pulsewidth( servo_V, func(max_V));
        
        message="ERROR: Angulo Vertical fora de faixa ["+str(min_V)+","+str(max_V)+"]"
        flash(message)
#https://stackoverflow.com/questions/71153840/how-to-flash-message-with-variables-in-flask
        
        return 0
        
    else:
        return 1
    
    

def Controle_Manual(angulo_H=0,angulo_V=0,slp=1): # 'angulo_H' [em graus] e 'angulo_V' [em graus] define o angulo de rotação e 'slp' o tempo entre comandos [em segundos]
       

    if(checa_angulo(angulo_H,angulo_V)):
       pwm.set_servo_pulsewidth( servo_H, func(float(angulo_H))) ;
       pwm.set_servo_pulsewidth( servo_V, func(float(angulo_V))) ;
       time.sleep( slp )

       #return func(float(angulo_H)), func(float(angulo_V)) 
           

def Controle_Manual_H(angulo_H,slp=1): # 'angulo_H' [em graus] define o angulo de rotação e 'slp' o tempo entre comandos [em segundos]
       
    if(checa_angulo(angulo_H)):
       pwm.set_servo_pulsewidth( servo_H, func(float(angulo_H))) ;
       time.sleep( slp )

       #return func(float(angulo_H))

def Controle_Manual_V(angulo_V,slp=1): # 'angulo_V' [em graus] define o angulo de rotação e 'slp' o tempo entre comandos [em segundos]
       
    if(checa_angulo(0,angulo_V)):
       pwm.set_servo_pulsewidth( servo_V, func(float(angulo_V))) ;
       time.sleep( slp )

       #return func(float(angulo_V))
           

def Varredura_Servos(x,passo=20): # 'x' equivale a tempo [em segundos] de varredura e 'passo' a quantidade de passos dentro do tempo 'x'

    meio_passo = passo/2
    for i in range(min_H, max_H, max_H/meio_passo):
        Controle_Manual_H(i, x/meio_passo)
    
    for i in range(max_H, min_H, -max_H/meio_passo):
        Controle_Manual_H(i, x/meio_passo)

    #return 0

#https://abyz.me.uk/rpi/pigpio/pdif2.html

        
def Center_Object_H(pos_H,Resolucao_H=640): # 'pos_H' [em pixel] e 'pos_V' [em pixel] definem o local do Objeto no plano da câmera e 'Resolucao_H' [em pixel] e 'Resolucao_V' [em pixel] a resolução da mesma

    Angulo_Atual=inv_func(pwm.get_servo_pulsewidth(servo_H)) 
    if pos_H>=Resolucao_H/2.0:
        Sinal=1.0
    else:
        Sinal=-1.0
    angulo_H=Angulo_Atual+Sinal*math.degrees(math.atan((math.fabs(pos_H-Resolucao_H/2.0)*Sx)/f))
    
    Controle_Manual_H(angulo_H,1)

    
def Center_Object_V(pos_V,Resolucao_V=480): # 'pos_H' [em pixel] e 'pos_V' [em pixel] definem o local do Objeto no plano da câmera e 'Resolucao_H' [em pixel] e 'Resolucao_V' [em pixel] a resolução da mesma

    Angulo_Atual=inv_func(pwm.get_servo_pulsewidth(servo_V)) 
    if pos_V>=Resolucao_V/2.0:
        Sinal=1.0
    else:
        Sinal=-1.0

    angulo_V=Angulo_Atual+Sinal*math.degrees(math.atan((math.fabs(pos_V-Resolucao_V/2.0)*Sx)/f))
    
    Controle_Manual_V(angulo_V,1)
    
    
def Center_Object(pos_H,pos_V,Resolucao_H=640,Resolucao_V=480): # 'pos_H' [em pixel] e 'pos_V' [em pixel] definem o local do Objeto no plano da câmera e 'Resolucao_H' [em pixel] e 'Resolucao_V' [em pixel] a resolução da mesma

    Angulo_Atual_H=inv_func(pwm.get_servo_pulsewidth(servo_H)) 
    Angulo_Atual_V=inv_func(pwm.get_servo_pulsewidth(servo_V)) 
    if pos_H>=Resolucao_H/2.0:
        Sinal_H=1.0
    else:
        Sinal_H=-1.0

    if pos_V>=Resolucao_V/2.0:
        Sinal_V=1.0
    else:
        Sinal_V=-1.0

    angulo_H=Angulo_Atual_H+Sinal_H*math.degrees(math.atan((1.0*math.fabs(pos_H-Resolucao_H/2.0)*Sx)/f))
    angulo_V=Angulo_Atual_V+Sinal_V*math.degrees(math.atan((1.0*math.fabs(pos_V-Resolucao_V/2.0)*Sx)/f))
    
    Controle_Manual(angulo_H,angulo_V,1)
        
#while True:
#    Controle_Manual_V(input("Rotacao_V: "),0.5)
