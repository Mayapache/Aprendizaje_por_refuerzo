# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 18:57:42 2025

@author: Mayapache
¡PirateⒶ y difunde!

"""

#%% Importar bibliotecas
import numpy as np
import matplotlib.pyplot as plt


#%%Programamos una máquina tragamonedas

n_tragamonedas=10 #Cantidad de palanquitas
acciones=np.arange(n_tragamonedas) #Acciones disponibles
q_real=np.random.normal(0,1,n_tragamonedas) #Las medias reales de cada palanquita
q_estimada=np.zeros((n_tragamonedas))  #El valor que estimamos de cada palanquita
n_veces_toma_accion=np.zeros((n_tragamonedas)) #La cantidad de veces que hemos bajado esa palanquita

pasos=1000


epsilon=0.1

for i in range(pasos):
    if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D probamos algo aleatoriamente
        eleccion=np.random.choice(acciones)
    else:
        #el primer elemento dentro de los valores maximos
        #eleccion=np.argmax(q_estimada)
        
        #un valor aleatorio dentro de los posibles elementos 
        posibles=np.where(q_estimada==max(q_estimada))[0]
        eleccion=np.random.choice(posibles,1)[0]

    recompensa=np.random.normal(q_real[eleccion],1)
    n_veces_toma_accion[eleccion]+=1
    q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]



#%%------- Ahora lo funcionalizamos y la mesa de pruebas propuesta por el libro


def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas)
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)

    return vec_recompensa,vec_optimo



n_tragamonedas=10
pasos=1000
epsilon=0.01

vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)

plt.figure()
plt.plot(vec_recompensa)
plt.show()

plt.figure()
plt.plot(vec_optimo)
plt.show()



#%% Ahora hacemos las 2000 pruebas / los 2000 tragamonedas diferentes

#Experimentos
n_tragamonedas=10
pasos=1000
n_muestras=2000

epsilon=0.01
mat_resultados_recompensa=np.zeros((n_muestras,pasos))
mat_resultados_optimo=np.zeros((n_muestras,pasos))
for i in range(n_muestras):
    vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
    mat_resultados_recompensa[i]=vec_recompensa
    mat_resultados_optimo[i]=vec_optimo

vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)

plt.figure()
plt.plot(vec_prom_recompensa)
plt.show()

plt.figure()
plt.plot(vec_prom_optimo)
plt.show()



#%%**************** funcionalizamos y realizamos los experimentos con los diferentes epsilons :D
#----------------- AQUI PRESENTA ------------------


def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas) 
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)

    return vec_recompensa,vec_optimo

def experimento_mesa_pruebas_tragamonedas(epsilon,pasos):
    #Experimentos
    n_tragamonedas=10
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    for i in range(n_muestras):
        vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_optimo
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo

pasos=5000

epsilon=0.01
vec_prom_recompensa_01,vec_prom_optimo_01=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0.1
vec_prom_recompensa_1,vec_prom_optimo_1=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0
vec_prom_recompensa_0,vec_prom_optimo_0=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)



plt.figure()
plt.title("Promedio de la recompensa")
plt.plot(vec_prom_recompensa_01)
plt.plot(vec_prom_recompensa_1)
plt.plot(vec_prom_recompensa_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige el valor óptimo")
plt.plot(vec_prom_optimo_01)
plt.plot(vec_prom_optimo_1)
plt.plot(vec_prom_optimo_0)
plt.show()


#%% Cosillas extra
#Ver punto de encuentro de los epsilons, :D listo, en 5000
#Ver cantidad de veces 2da mejor opcion
#Ver la varianza

n_tragamonedas=10
n_muestras=2000
epsilon=0.1
pasos=1000

i=0
def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas)
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_ranking=np.zeros((pasos))
    rank=np.argsort(np.argsort(q_real))

    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        #vec_ranking[i]=eleccion==np.argmax(q_real)
        vec_ranking[i]=n_tragamonedas-rank[eleccion]
        

    return vec_recompensa,vec_ranking


def experimento_mesa_pruebas_tragamonedas(epsilon,pasos):
    #Experimentos
    n_tragamonedas=10
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    mat_resultados_2do_mejor=np.zeros((n_muestras,pasos))
    
    for i in range(n_muestras):
        vec_recompensa,vec_ranking=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_ranking==1
        mat_resultados_2do_mejor[i]=vec_ranking==2
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    vec_prom_2do_mejor=np.mean(mat_resultados_2do_mejor,axis=0)
    vec_desv_rec=np.std(mat_resultados_recompensa,axis=0)
    vec_desv_optimo=np.std(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo,vec_prom_2do_mejor, vec_desv_rec, vec_desv_optimo


pasos=1000

epsilon=0.01
vec_prom_recompensa_01,vec_prom_optimo_01,vec_prom_2do_mejor_01, vec_desv_rec_01, vec_desv_optimo_01=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0.1
vec_prom_recompensa_1,vec_prom_optimo_1,vec_prom_2do_mejor_1, vec_desv_rec_1, vec_desv_optimo_1=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0
vec_prom_recompensa_0,vec_prom_optimo_0,vec_prom_2do_mejor_0, vec_desv_rec_0, vec_desv_optimo_0=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)



plt.figure()
plt.title("Promedio de la recompensa")
plt.plot(vec_prom_recompensa_01)
plt.plot(vec_prom_recompensa_1)
plt.plot(vec_prom_recompensa_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige valor óptimo")
plt.plot(vec_prom_optimo_01)
plt.plot(vec_prom_optimo_1)
plt.plot(vec_prom_optimo_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige el segundo mejor valor")
plt.plot(vec_prom_2do_mejor_01)
plt.plot(vec_prom_2do_mejor_1)
plt.plot(vec_prom_2do_mejor_0)
plt.show()

plt.figure()
plt.title("Desviacion estándar de la recompensa")
plt.plot(vec_desv_rec_01)
plt.plot(vec_desv_rec_1)
plt.plot(vec_desv_rec_0)
plt.show()

plt.figure()
plt.title("Desviación estándar del optimo")
plt.plot(vec_desv_optimo_01)
plt.plot(vec_desv_optimo_1)
plt.plot(vec_desv_optimo_0)
plt.show()



#--------- Ver con una distribución diferente de los centros de las palanquitas

n_tragamonedas=10
n_muestras=2000
epsilon=0.1
pasos=1000

i=0
def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas)
    q_real=np.random.random(n_tragamonedas)*2-1
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_ranking=np.zeros((pasos))
    rank=np.argsort(np.argsort(q_real))

    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        #vec_ranking[i]=eleccion==np.argmax(q_real)
        vec_ranking[i]=n_tragamonedas-rank[eleccion]
        

    return vec_recompensa,vec_ranking


def experimento_mesa_pruebas_tragamonedas(epsilon,pasos):
    #Experimentos
    n_tragamonedas=10
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    mat_resultados_2do_mejor=np.zeros((n_muestras,pasos))
    
    for i in range(n_muestras):
        vec_recompensa,vec_ranking=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_ranking==1
        mat_resultados_2do_mejor[i]=vec_ranking==2
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    vec_prom_2do_mejor=np.mean(mat_resultados_2do_mejor,axis=0)
    vec_desv_rec=np.std(mat_resultados_recompensa,axis=0)
    vec_desv_optimo=np.std(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo,vec_prom_2do_mejor, vec_desv_rec, vec_desv_optimo


pasos=1000

epsilon=0.01
vec_prom_recompensa_01,vec_prom_optimo_01,vec_prom_2do_mejor_01, vec_desv_rec_01, vec_desv_optimo_01=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0.1
vec_prom_recompensa_1,vec_prom_optimo_1,vec_prom_2do_mejor_1, vec_desv_rec_1, vec_desv_optimo_1=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0
vec_prom_recompensa_0,vec_prom_optimo_0,vec_prom_2do_mejor_0, vec_desv_rec_0, vec_desv_optimo_0=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)



plt.figure()
plt.title("Promedio de la recompensa, otra dist.")
plt.plot(vec_prom_recompensa_01)
plt.plot(vec_prom_recompensa_1)
plt.plot(vec_prom_recompensa_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige valor óptimo, otra dist.")
plt.plot(vec_prom_optimo_01)
plt.plot(vec_prom_optimo_1)
plt.plot(vec_prom_optimo_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige el segundo mejor valor, otra dist.")
plt.plot(vec_prom_2do_mejor_01)
plt.plot(vec_prom_2do_mejor_1)
plt.plot(vec_prom_2do_mejor_0)
plt.show()

plt.figure()
plt.title("Desviacion estándar de la recompensa, otra dist.")
plt.plot(vec_desv_rec_01)
plt.plot(vec_desv_rec_1)
plt.plot(vec_desv_rec_0)
plt.show()

plt.figure()
plt.title("Desviación estándar del optimo, otra dist.")
plt.plot(vec_desv_optimo_01)
plt.plot(vec_desv_optimo_1)
plt.plot(vec_desv_optimo_0)
plt.show()



#------------- con entorno dinámico, cambio en la posicion 500


def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas) 
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        if i==500:
            q_real=np.random.normal(0,1,n_tragamonedas)
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)

    return vec_recompensa,vec_optimo

def experimento_mesa_pruebas_tragamonedas(epsilon,pasos):
    #Experimentos
    n_tragamonedas=10
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    for i in range(n_muestras):
        vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_optimo
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo

pasos=1000

epsilon=0.01
vec_prom_recompensa_01,vec_prom_optimo_01=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0.1
vec_prom_recompensa_1,vec_prom_optimo_1=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0
vec_prom_recompensa_0,vec_prom_optimo_0=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)



plt.figure()
plt.title("Promedio de la recompensa")
plt.plot(vec_prom_recompensa_01)
plt.plot(vec_prom_recompensa_1)
plt.plot(vec_prom_recompensa_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige el valor óptimo")
plt.plot(vec_prom_optimo_01)
plt.plot(vec_prom_optimo_1)
plt.plot(vec_prom_optimo_0)
plt.show()



#----------- entorno dinámico, cambio gradual de las palanquitas, acorde se usan :D

def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon):
    acciones=np.arange(n_tragamonedas) 
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            #eleccion=np.argmax(q_estimada)
            
            #un valor aleatorio dentro de los posibles elementos 
            posibles=np.where(q_estimada==max(q_estimada))[0]
            eleccion=np.random.choice(posibles,1)[0]

        recompensa=np.random.normal(q_real[eleccion],1)
        n_veces_toma_accion[eleccion]+=1
        q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)
        
        q_real[eleccion]-=0.05

    return vec_recompensa,vec_optimo

def experimento_mesa_pruebas_tragamonedas(epsilon,pasos):
    #Experimentos
    n_tragamonedas=10
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    for i in range(n_muestras):
        vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_optimo
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo

pasos=1000

epsilon=0.01
vec_prom_recompensa_01,vec_prom_optimo_01=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0.1
vec_prom_recompensa_1,vec_prom_optimo_1=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)

epsilon=0
vec_prom_recompensa_0,vec_prom_optimo_0=experimento_mesa_pruebas_tragamonedas(epsilon,pasos)



plt.figure()
plt.title("Promedio de la recompensa, cambio gradual")
plt.plot(vec_prom_recompensa_01)
plt.plot(vec_prom_recompensa_1)
plt.plot(vec_prom_recompensa_0)
plt.show()

plt.figure()
plt.title("Porcentaje de veces elige el valor óptimo, cambio gradual")
plt.plot(vec_prom_optimo_01)
plt.plot(vec_prom_optimo_1)
plt.plot(vec_prom_optimo_0)
plt.show()







#%% Valores iniciales optimistas



def experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=2):
    #Experimentos
    pasos=1000
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    
    for i in range(n_muestras):
        vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon,bias_inicial,alfa)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_optimo
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo


def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon,bias_inicial,alfa):
    acciones=np.arange(n_tragamonedas)
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))+bias_inicial
    #q_estimada=val_inicial
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        if np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            eleccion=np.argmax(q_estimada)
            #un valor aleatorio dentro de los posibles elementos 
            #posibles=np.where(q_estimada==max(q_estimada))[0]
            #eleccion=np.random.choice(posibles,1)[0]

        recompensa=q_real[eleccion]+np.random.normal(0,1)
        
        if alfa==2:
            n_veces_toma_accion[eleccion]+=1
            q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        else:
            q_estimada[eleccion]=q_estimada[eleccion]+alfa*(recompensa-q_estimada[eleccion])
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)

    return vec_recompensa,vec_optimo


n_tragamonedas=10
'''
bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
alfa=.8
vec_prom_recompensa_1_0,vec_prom_optimo_1_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

plt.figure()
plt.plot(vec_prom_recompensa_1_0)
plt.show()

bias_inicial=np.zeros((n_tragamonedas))
epsilon=0
alfa=2
vec_prom_recompensa_0_0,vec_prom_optimo_0_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)
plt.figure()
plt.plot(vec_prom_recompensa_0_0)
plt.show()




alfa=2

bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
vec_prom_recompensa_1_0,vec_prom_optimo_1_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))+5
epsilon=0.1
vec_prom_recompensa_1_5,vec_prom_optimo_1_5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))
epsilon=0
vec_prom_recompensa_0_0,vec_prom_optimo_0_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))+5
epsilon=0
vec_prom_recompensa_0_5,vec_prom_optimo_0_5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

#azul, naranja, verde, rojo

plt.figure()
plt.plot(vec_prom_recompensa_1_0)
plt.plot(vec_prom_recompensa_1_5)
plt.plot(vec_prom_recompensa_0_0)
plt.plot(vec_prom_recompensa_0_5)
plt.show()

plt.figure()
plt.plot(vec_prom_optimo_1_0)
plt.plot(vec_prom_optimo_1_5)
plt.plot(vec_prom_optimo_0_0)
plt.plot(vec_prom_optimo_0_5)
plt.show()

alfa=.1
alfa=.5

bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
vec_prom_recompensa_1_0,vec_prom_optimo_1_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))+5
epsilon=0.1
vec_prom_recompensa_1_5,vec_prom_optimo_1_5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))
epsilon=0
vec_prom_recompensa_0_0,vec_prom_optimo_0_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))+5
epsilon=0
vec_prom_recompensa_0_5,vec_prom_optimo_0_5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)





plt.figure()
plt.plot(vec_prom_recompensa_1_0)
plt.plot(vec_prom_recompensa_1_5)
plt.plot(vec_prom_recompensa_0_0)
plt.plot(vec_prom_recompensa_0_5)
plt.show()

plt.figure()
plt.plot(vec_prom_optimo_1_0)
plt.plot(vec_prom_optimo_1_5)
plt.plot(vec_prom_optimo_0_0)
plt.plot(vec_prom_optimo_0_5)
plt.show()

'''

# --- Del libro :D

alfa=0.1
bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
vec_prom_recompensa_1_0,vec_prom_optimo_1_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

bias_inicial=np.zeros((n_tragamonedas))+5
epsilon=0
vec_prom_recompensa_1_5,vec_prom_optimo_1_5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)

# --------------------- el pesimista 
alfa=0.1
bias_inicial=np.zeros((n_tragamonedas))-5
epsilon=0.1
vec_prom_recompensa_1_m5,vec_prom_optimo_1_m5=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa)


plt.figure()
plt.title("Promedio de la recompensa, con valores optimistas y pesimistas")
plt.plot(vec_prom_recompensa_1_0)
plt.plot(vec_prom_recompensa_1_5)
plt.plot(vec_prom_recompensa_1_m5)
plt.show()

plt.figure()
plt.title("Porcentaje veces elige valor optimo, con valores optimistas y pesimistas")
plt.plot(vec_prom_optimo_1_0)
plt.plot(vec_prom_optimo_1_5)
plt.plot(vec_prom_optimo_1_m5)
plt.show()





#%%Selección de acción por límite superior de confianza





def experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=2,c=-1):
    #Experimentos
    pasos=1000
    n_muestras=2000
    mat_resultados_recompensa=np.zeros((n_muestras,pasos))
    mat_resultados_optimo=np.zeros((n_muestras,pasos))
    
    for i in range(n_muestras):
        vec_recompensa,vec_optimo=mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon,bias_inicial,alfa,c)
        mat_resultados_recompensa[i]=vec_recompensa
        mat_resultados_optimo[i]=vec_optimo
    
    vec_prom_recompensa=np.mean(mat_resultados_recompensa,axis=0)
    vec_prom_optimo=np.mean(mat_resultados_optimo,axis=0)
    
    return vec_prom_recompensa,vec_prom_optimo

def mesa_pruebas_tragamonedas(n_tragamonedas,pasos,epsilon,bias_inicial,alfa,c):
    acciones=np.arange(n_tragamonedas)
    q_real=np.random.normal(0,1,n_tragamonedas)
    q_estimada=np.zeros((n_tragamonedas))+bias_inicial
    #q_estimada=val_inicial
    n_veces_toma_accion=np.zeros((n_tragamonedas))
    
    vec_recompensa=np.zeros((pasos))
    vec_optimo=np.zeros((pasos))
    
    
    for i in range(pasos):
        
        if c>0:
            eleccion=np.argmax(q_estimada+c*np.sqrt(np.log(i)/n_veces_toma_accion))
        
        elif np.random.random(1)[0]<epsilon: #Si no greedy, exploramos :D
            eleccion=np.random.choice(acciones)
        else:
            #el primer elemento dentro de los valores maximos
            eleccion=np.argmax(q_estimada)
            #un valor aleatorio dentro de los posibles elementos 
            #posibles=np.where(q_estimada==max(q_estimada))[0]
            #eleccion=np.random.choice(posibles,1)[0]

        recompensa=q_real[eleccion]+np.random.normal(0,1)
        
        if alfa==2:
            n_veces_toma_accion[eleccion]+=1
            q_estimada[eleccion]=(q_estimada[eleccion]*(n_veces_toma_accion[eleccion]-1)+recompensa)/n_veces_toma_accion[eleccion]
        else:
            q_estimada[eleccion]=q_estimada[eleccion]+alfa*(recompensa-q_estimada[eleccion])
        
        vec_recompensa[i]=recompensa
        vec_optimo[i]=eleccion==np.argmax(q_real)

    return vec_recompensa,vec_optimo




n_tragamonedas=10

alfa=2
bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
c=2
vec_prom_recompensa_2_0,vec_prom_optimo_2_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa,c=c)

alfa=2
bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
c=1
vec_prom_recompensa_1_0,vec_prom_optimo_1_0=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa,c=c)


alfa=2
bias_inicial=np.zeros((n_tragamonedas))
epsilon=0.1
c=-1
vec_prom_recompensa_0_1,vec_prom_optimo_0_1=experimento_mesa_pruebas_tragamonedas(epsilon, bias_inicial,n_tragamonedas,alfa=alfa,c=c)






#azul, naranja, verde, rojo
plt.figure()
plt.title("Promedio recompensa con UBAS")
plt.plot(vec_prom_recompensa_2_0)
plt.plot(vec_prom_recompensa_1_0)
plt.plot(vec_prom_recompensa_0_1)
plt.show()

plt.figure()
plt.title("Promedio recompensa con UBAS")
plt.plot(vec_prom_optimo_2_0)
plt.plot(vec_prom_optimo_1_0)
plt.plot(vec_prom_optimo_0_1)
plt.show()





