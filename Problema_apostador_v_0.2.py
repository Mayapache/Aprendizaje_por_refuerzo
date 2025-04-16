# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 17:38:19 2025

@author: Mayapache
¡PirateⒶ y difunde!

Value iteration sobre el problema del apostador :D

Inicializa
Evalua política
Mejora política


"""


#%% Importamos librerías
import numpy as np
import matplotlib.pyplot as plt


#%% Definimos ambiente

'''
Esto namás fue pa ver si se podía y q tan fácil era, basado en gymnasium
'''

class ambiente_apostador():
    def __init__(self, dinero_actual=50):
        self.prob_exito=0.4
        self.dinero_meta=100
        self.dinero_jugador= dinero_actual #El estado :D
        
    def _observacion(self):
        return {"dinero_jugador": self.dinero_jugador}
    def reset(self, dinero_actual=50):
        self.dinero_jugador= dinero_actual

    
    def paso(self, dinero_apostado):
        
        if np.random.random()<self.prob_exito:
            self.dinero_jugador+=dinero_apostado
        else:
            self.dinero_jugador-=dinero_apostado
        
        
        observacion=self._observacion()
        
        if self.dinero_jugador>=self.dinero_meta:
            recompensa=1
        else:
            recompensa=0
        
        if self.dinero_jugador>=self.dinero_meta or self.dinero_jugador<=0:
            terminado=True
        else:
            terminado=False
            
        truncado=False
        
        return observacion, recompensa, terminado, truncado


ambiente=ambiente_apostador()
ambiente._observacion()
ambiente.paso(30)

ambiente.reset()

#%% Empieza programa

#%%% Primer intento

'''
Spoiler: no funcionó

Se define un cubo de transiciones con 3 ejes, el valor es la probabilidad de transición:
    Estado actual
    Estado siguiente
    Accion tomada

'''
#------------------------Inicializamos cosillas

#Definimos cubo de transiciones entre estados dependiendo de la acción tomada

#Objetivo, ganar 100 varitos
#no se puede apostar más de lo que es necesario para ganar 100
    #ej.: de tener 70, el máximo a apostar son 30
#no se puede apostar lo que no se tiene
#Recompensa +1 al llegar a 100, 0 de cualquier otra forma


#[Estado origen] [Estado destino] [accion tomada]
#[1-99] [0-100] [1-99]
prob_ganar=0.4

cubo_dinamica_apostador=np.zeros((99,101,99))

for i in range(len(cubo_dinamica_apostador)): #Estado origen
    for j in range(len(cubo_dinamica_apostador[0])): #Estado destino
        for k in range(len(cubo_dinamica_apostador[0][0])): #Dinero apostado
                #dinero apostado es menor al dinero disponible, y estado destino= estado actual + dinero apostado
            if (i>=k) and j==((i+1)+(k+1)):
                cubo_dinamica_apostador[i][j][k]=prob_ganar
            if (i>=k) and j==((i+1)-(k+1)) and ((i+1)+(k+1))<=100:
                cubo_dinamica_apostador[i][j][k]=1-prob_ganar

edo_origen=99
edo_destino=100
apuesta=99
cubo_dinamica_apostador[edo_origen-1][edo_destino][apuesta-1]


#Inicializamos, por el momento, en ceros, la funcion de valor y la politica propuesta

pi=np.zeros(99)
funcion_valor=np.zeros(101)


umbral_cambio_evaluacion_politica=0.0001
gamma=1

#Variable que checa si la politica q tenemos ya se estabilizó
politica_estable=False
#Contador, namas pa saber cuanto se tarda:
cant_iteraciones=0

while not politica_estable: #Mientras la política no sea estable
    cant_iteraciones+=1
    
    cambio=umbral_cambio_evaluacion_politica + 1 #Pa q entre al while
    while cambio > umbral_cambio_evaluacion_politica :
        cambio=0
        nu_funcion_valor=np.zeros(101)
        # 1 Evaluación de política 
        for i in range(len(cubo_dinamica_apostador)): # Para cada uno de los estados origen
            sumita=0
            for j in range(len(cubo_dinamica_apostador[0])):
                if j==100:
                    recompensa=10000000
                else:
                    recompensa=0
                sumita+=cubo_dinamica_apostador[i][j][int(pi[i])]*(recompensa + gamma*funcion_valor[j])
            cambio=np.max([np.abs(funcion_valor[i+1]-sumita), cambio])
            nu_funcion_valor[i+1]=sumita
        funcion_valor=nu_funcion_valor

    
    
    
    # Mejora de política
    
    politica_estable=True
    for i in range(len(cubo_dinamica_apostador)): # Para cada uno de los estados origen
        a=pi[i]
        for j in range(len(cubo_dinamica_apostador[0])): # para cada uno de los estados destino :D
            if j==100:
                recompensa=1
            else:
                recompensa=0
            vec_q=np.zeros(len(cubo_dinamica_apostador[0][0]))
            for k in range(len(cubo_dinamica_apostador[0][0])):
                vec_q[k]=cubo_dinamica_apostador[i][j][k]*(recompensa + gamma*funcion_valor[j])    
        mejor_a=vec_q.argmax()
        pi[i]=mejor_a
        if a!=pi[i]:
            politica_estable=False
    

plt.figure()
plt.plot(funcion_valor)
plt.show()

plt.figure()
plt.plot(pi)
plt.show()



#%%---------------- Segunda prueba
'''
Spoiler: no funcionó tampoco

-Nos deshacemos del cubo del ambiente
-Aumentamos la  precisión en la evaluación

'''



umbral_cambio_evaluacion_politica=1e-22

pi=np.zeros(99)
funcion_valor=np.zeros(101)

gamma=1

politica_estable=False
cant_iteraciones=0


#Evaluación de política


politica_estable=False
while not politica_estable:
    
    cambio=umbral_cambio_evaluacion_politica+1
    while cambio>umbral_cambio_evaluacion_politica:
        cambio=0
        for i in range(len(cubo_dinamica_apostador)): #Para cada estado s en S
            v_iejita=funcion_valor[i+1]
            if (i+1+pi[i]+1)==100:
                recompensa=1
            else:
                recompensa=0
            funcion_valor[i+1]=prob_ganar* (recompensa + gamma*funcion_valor[int(i+1+pi[i]+1)]) + (1-prob_ganar)* (gamma*funcion_valor[int(i+1-pi[i]-1)])
            
            cambio=np.max([cambio, np.abs(v_iejita-funcion_valor[i+1])])
    
    
    politica_estable=True
    
    for i in range(len(cubo_dinamica_apostador)): #Para cada estado s en S
        a_viejita=pi[i]
        
        vec_q=np.zeros(len(pi))
        for k in range(len(pi)):
            if (k+1 + i+1 <=100) and k<=i:
                if (i+1+k+1)==100:
                    recompensa=1
                else:
                    recompensa=0
                vec_q[k]=prob_ganar* (recompensa + gamma*funcion_valor[int(i+1+k+1)]) + (1-prob_ganar)* (gamma*funcion_valor[int(i+1-k-1)])
            
            
        mejor_a=vec_q.argmax()
        pi[i]=mejor_a
        if a_viejita != pi[i]:
            politica_estable=False


plt.figure()
plt.plot(pi)
plt.show()

plt.figure()
plt.plot(funcion_valor)
plt.show()



#%%---------------- Tercera prueba
'''
Spoiler: no funcionó

Reestructuración del programa, se funcionaliza bellman, array de recompensa

Sospecha de la precisión en el tipo de dato, pequeñas pruebas

'''


p_ganar=0.4
gamma=1


recompensas=np.zeros(101) #del 0 al 100
recompensas[100]=1
#recompensas[100]=1e12
#recompensas[100]=1e40

funcion_valor=np.zeros(101) #Funcion de valor para cada estado
pi=np.zeros(100) #política pi para cada estado


#Definimos la ec de bellman :D
def bellman(estado,accion,funcion_valor):
    return p_ganar*(recompensas[estado+accion] + gamma* funcion_valor[estado+accion])+ (1-p_ganar)*(recompensas[estado-accion] + gamma* funcion_valor[estado-accion])

#Evaluación política
umbral_cambio_evaluacion_politica=1e-4
#umbral_cambio_evaluacion_politica=1e-22
#umbral_cambio_evaluacion_politica=1e-40


contador=0

politica_estable=False
while not politica_estable:
    contador+=1
    
    #Evaluación de política
    while True:
        cambio=0
        for estado in range(100): #Pa todos los estados 
            v_iejita=funcion_valor[estado] #Guardamos valor pa comparar
            funcion_valor[estado]=bellman(int(estado),int(pi[estado]),funcion_valor) #Obtenemos nuevo valor
            cambio=np.max([cambio,np.abs(funcion_valor[estado]-v_iejita)]) #Obtenemos el cambio
        if cambio < umbral_cambio_evaluacion_politica: #Si el cambio ya es menor que el umbral, rompemos el while
            break
    
    #Mejora de política    
    politica_estable=True
    for estado in range(1,100): #del 1 al 99
        a_viejita=pi[estado] #Guardamos la viejita, pa ver estabilidad
        maximo_accion=min(estado, 100-estado) #El máximo de acción posible, el mínimo entre el estado en elq ue estamos y el varo q falta pa 100
        vec_q=np.zeros(maximo_accion+1) #vectorcito de los valores de q(s,a)
        for accion in range(1,maximo_accion+1): #desde la acción 1, hasta el máximo apostable
            vec_q[accion]=bellman(int(estado),int(accion),funcion_valor) #Guardamos en vec_q
        pi[estado]=np.argmax(vec_q) #Papas, tomamos el máximo :D la posición del array coincide con el dinero apostado
        
        if a_viejita!=pi[estado]: #Indicamos si hubo cambio en la política (política no estable)
            politica_estable=False

plt.figure()
plt.show()
plt.plot(pi)

plt.figure()
plt.plot(funcion_valor)
plt.show()



#%%Cuarto intento, D: q funcione ya parfavar
import decimal as dc

'''
La precisión sí es EL problema

:D Está vivo

'''

p_ganar=dc.Decimal(0.4)
p_ganar=dc.Decimal('0.4')
gamma=dc.Decimal(1)

#recompensas=np.zeros(101) #del 0 al 100
recompensas=[dc.Decimal(0)]*101

recompensas[100]=1

#funcion_valor=np.zeros(101) #Funcion de valor para cada estado
funcion_valor=[dc.Decimal(0)]*101

pi=np.zeros(100) #política pi para cada estado


#Definimos la ec de bellman :D
def bellman(estado,accion,funcion_valor):
    return p_ganar*(recompensas[estado+accion] + gamma* funcion_valor[estado+accion])+ (1-p_ganar)*(recompensas[estado-accion] + gamma* funcion_valor[estado-accion])

#Evaluación política
umbral_cambio_evaluacion_politica=0.1
#umbral_cambio_evaluacion_politica=1e-4
#umbral_cambio_evaluacion_politica=1e-16

contador=0
vec_cuentas_evaluacion=[]

politica_estable=False
while not politica_estable:
    contador+=1
    
    cont_eval=0
    while True:
        cont_eval+=1
        cambio=0
        for estado in range(100):
            v_iejita=funcion_valor[estado]
            funcion_valor[estado]=bellman(int(estado),int(pi[estado]),funcion_valor)
            cambio=np.max([cambio,np.abs(funcion_valor[estado]-v_iejita)])
        if cambio < umbral_cambio_evaluacion_politica:
            break
    vec_cuentas_evaluacion.append(cont_eval)
    #Mejora de política
    
    politica_estable=True
    
    for estado in range(1,100): #del 1 al 99
        a_viejita=pi[estado]
        maximo_accion=min(estado, 100-estado)
        vec_q=np.zeros(maximo_accion+1)
        for accion in range(1,maximo_accion+1):
            vec_q[accion]=bellman(int(estado),int(accion),funcion_valor)
        pi[estado]=np.argmax(vec_q)
        
        if a_viejita!=pi[estado]:
            politica_estable=False



plt.figure()
plt.plot(pi)
plt.show()

plt.figure()
plt.plot(funcion_valor)
plt.show()


#%% otro intento :D pero ahora con value iteration

'''
Spoiler: no funcionó

'''



p_ganar=dc.Decimal('0.4')
gamma=dc.Decimal(1)

#recompensas=np.zeros(101) #del 0 al 100
recompensas=[dc.Decimal(0)]*101

recompensas[100]=1
#recompensas[100]=10
#recompensas[100]=100
#recompensas[100]=dc.Decimal('100')
#recompensas[100]=dc.Decimal('1e20')

#funcion_valor=np.zeros(101) #Funcion de valor para cada estado
funcion_valor=[dc.Decimal(0)]*101

pi=np.zeros(100) #política pi para cada estado


#Definimos la ec de bellman :D
def bellman(estado,accion,funcion_valor):
    return p_ganar*(recompensas[estado+accion] + gamma* funcion_valor[estado+accion])+ (1-p_ganar)*(recompensas[estado-accion] + gamma* funcion_valor[estado-accion])

#Value iteration

umbral_cambio_evaluacion_politica=1e-4
#umbral_cambio_evaluacion_politica=1e-16
#umbral_cambio_evaluacion_politica=1e-50
#umbral_cambio_evaluacion_politica=1e-100
#umbral_cambio_evaluacion_politica=1e-200
#umbral_cambio_evaluacion_politica=dc.Decimal('1e-200')


contador=0
vec_cambio=[]
while True:
    contador+=1
    cambio=0
    for estado in range(100):
        v_iejita=funcion_valor[estado]
        
        maximo_accion=min(estado, 100-estado)
        vec_q=np.zeros(maximo_accion+1)
        for accion in range(1,maximo_accion+1):
            vec_q[accion]=bellman(int(estado),int(accion),funcion_valor)
        
        funcion_valor[estado]=dc.Decimal(np.max(vec_q)) #Probablemente aquí esté el problema de precisión ¿?
        cambio=np.max([cambio,np.abs(funcion_valor[estado]-v_iejita)])
    vec_cambio.append(cambio)
    if cambio < umbral_cambio_evaluacion_politica:
        break



#Extraemos la política pi :D
for estado in range(1,100): #del 1 al 99
    maximo_accion=min(estado, 100-estado)
    vec_q=np.zeros(maximo_accion+1)
    for accion in range(1,maximo_accion+1):
        vec_q[accion]=bellman(int(estado),int(accion),funcion_valor)
    pi[estado]=np.argmax(vec_q)



plt.figure()
plt.plot(pi)
plt.show()

plt.figure()
plt.plot(funcion_valor)
plt.show()


#%% Segundo  intento de value iteration :D 

'''
cambiamos el max :D

'''



p_ganar=dc.Decimal('0.4')
gamma=dc.Decimal(1)

#recompensas=np.zeros(101) #del 0 al 100
recompensas=[dc.Decimal(0)]*101

recompensas[100]=1
#recompensas[100]=10
#recompensas[100]=100

#recompensas[100]=dc.Decimal('100')
recompensas[100]=dc.Decimal('1e12')

#funcion_valor=np.zeros(101) #Funcion de valor para cada estado
funcion_valor=[dc.Decimal(0)]*101

pi=np.zeros(100) #política pi para cada estado


#Definimos la ec de bellman :D
def bellman(estado,accion,funcion_valor):
    return p_ganar*(recompensas[estado+accion] + gamma* funcion_valor[estado+accion])+ (1-p_ganar)*(recompensas[estado-accion] + gamma* funcion_valor[estado-accion])

#Value iteration

umbral_cambio_evaluacion_politica=1e-4
#umbral_cambio_evaluacion_politica=1e-16
#umbral_cambio_evaluacion_politica=1e-50
#umbral_cambio_evaluacion_politica=1e-100
#umbral_cambio_evaluacion_politica=1e-200
#umbral_cambio_evaluacion_politica=dc.Decimal('1e-200')


contador=0
vec_cambio=[]
while True:
    contador+=1
    cambio=0
    for estado in range(100):
        v_iejita=funcion_valor[estado]
        
        maximo_accion=min(estado, 100-estado)
        #vec_q=np.zeros(maximo_accion+1)
        vec_q=[dc.Decimal(0)]*(maximo_accion+1)
        for accion in range(1,maximo_accion+1):
            vec_q[accion]=bellman(int(estado),int(accion),funcion_valor)
        
        funcion_valor[estado]=dc.Decimal(max(vec_q)) #Probablemente aquí esté el problema de precisión ¿?
        cambio=np.max([cambio,np.abs(funcion_valor[estado]-v_iejita)])
    vec_cambio.append(cambio)
    if cambio < umbral_cambio_evaluacion_politica:
        break



#Extraemos la política pi :D
for estado in range(1,100): #del 1 al 99
    maximo_accion=min(estado, 100-estado)
    vec_q=np.zeros(maximo_accion+1)
    for accion in range(1,maximo_accion+1):
        vec_q[accion]=bellman(int(estado),int(accion),funcion_valor)
    pi[estado]=np.argmax(vec_q)



plt.figure()
plt.plot(pi)
plt.show()

plt.figure()
plt.plot(funcion_valor)
plt.show()





























