#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:19:22 2022

@author: ana
"""
# -*- coding: utf-8 -*-
import random
from multiprocessing import Process
from multiprocessing import Array
from multiprocessing import BoundedSemaphore, Semaphore




NPROD = 6
listaProd= [7] * NPROD
NCONS = 1


def minimo(lista):
    aux = [0]*len(lista)
    maximo = max(lista)
    for i in range(len(lista)):
        if lista[i] == -1:
            aux[i] = maximo + 1
        else:
            aux[i] = lista[i]
            
    minimo = aux[0]
    index = 0
    
    for i in range(1, len(aux)):
        if aux[i] < minimo and aux[i] != -1:
            minimo = aux[i]
            index = i
            
    return minimo, index

    

def productor(lista, buffer, index,limite):
    
     v = 0
     
     for k in range(limite):
         v += random.randint(0,5)
         print('prod:', index, 'iter:', k, 'v:', v)
         lista[2*index].acquire() 
         buffer[index] = v
         lista[2*index+1].release() 
     
     v = -1
     lista[2*index].acquire() 
     buffer[index] = v
     lista[2*index+1].release() 
     


def consumidor(lista, buffer):  
    
    numeros = []
    
    for i in range(NPROD):
        lista[2*i+1].acquire() 
        
    while [-1]*NPROD != list(buffer):
        
        v, index = minimo(buffer)
        print('añade:', v, 'de Prod', index)
        numeros.append(v)
        print (f"numeros: {numeros}")
        lista[2*index].release()
        lista[2*index + 1].acquire() 
    
    print ('Valor final de la lista:', numeros)
    
    

def main():
     buffer = Array('i', NPROD)
    
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(1))
         lista_sem.append(Semaphore(0)) 
     
     lp = []
     
     for index in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, buffer, index, listaProd[index])))
     lp.append(Process(target=consumidor, args=(lista_sem, buffer)))    
     
     for p in lp:
         p.start()
     for p in lp:
         p.join()


if __name__ == "__main__":
 main()  

 