import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal

# Declaracion de variables
distanciaPicos = 0
arrayInflexion = [0, 0, 0]
arrayPicos = []
arrayPosicionesPicos = []
arrayDistanciaPicos = []

# Se obtiene la senial desde un archivo .csv alojado 
# en la misma carpeta que el Analizador.py
header = ['Tiempo', 'Senial']
data = pd.read_csv('data_3.csv', names=header)
arrayElectro = data['Senial']

# Saca la frecuencia cardiaca 
def determinarFrecuencia(posicion):

    global distanciaPicos
    fs = 0.004

    if(hayUnPico(posicion)):
        arrayDistanciaPicos.append(round(distanciaPicos * fs, 3))
        distanciaPicos = 0
    else: 
        distanciaPicos += 1 
        

# Determina los puntos de inflexion 
def hayUnPico(posicion):
    
    if(arrayInflexion[1] >= 0.1):
        if(arrayInflexion[0] < arrayInflexion[1] and arrayInflexion[1] > arrayInflexion[2]):
            arrayPosicionesPicos.append(posicion - 1)
            arrayPicos.append(round(arrayInflexion[1], 3)); 
            return True
        else:
            return False


# Inicializa el array de puntos de inflexion     
def setArrayInflexion(valorActual):
    
    if(len(arrayInflexion) == 3):
        arrayInflexion.pop(0)
        
    arrayInflexion.append(valorActual)  

# Filtros ----------------------------------------
def filtroPasaBajos(senial):
    
    N = 1    
    Wn = 0.08
    b, a = signal.butter(N, Wn, 'lowpass', output='ba')
    senialFiltrada = signal.filtfilt(b, a, senial)
    return senialFiltrada   

def filtroPasaAltos(senial):
    
    N = 1    
    Wn = 0.08 
    b, a = signal.butter(N, Wn, 'highpass', output='ba')
    senialFiltrada = signal.filtfilt(b, a, senial)
    return senialFiltrada 
# Filtros ----------------------------------------
  
# Diagnostica la senial segun la frecuencia  
def analizarFrecuencia(frecuencia):
    
    if(frecuencia < 60):
        print "Analisis: Posible bradicardia"
    elif(frecuencia >= 60 and frecuencia <= 100):
        print "Analisis: Frecuencia normal"  
    else:
        print "Analisis: Posible taquicardia"


def comenzarAnalisis():
    
    posicion = 0
    for valorActual in filtroPasaBajos(filtroPasaAltos(arrayElectro)):
    
        setArrayInflexion(valorActual)
        determinarFrecuencia(posicion)
        posicion += 1


# Arranca el programa 
comenzarAnalisis()

# Grafica el electro
plt.plot(arrayElectro)
plt.plot(arrayPosicionesPicos, arrayPicos, 'go')
plt.plot(filtroPasaBajos(filtroPasaAltos(arrayElectro)), 'r-', linewidth=2)
plt.legend(['Original', 'Picos R', 'Filtrada'])
plt.title('Analizador ECG')
plt.show()

# Imprime los datos
frecuenciaCardiaca = round(60 / np.average(arrayDistanciaPicos), 2);
analizarFrecuencia(frecuenciaCardiaca)
print "Frecuencia cardiaca:", frecuenciaCardiaca, "bpm."
print "Amplitud picos R:", arrayPicos  
print "Distancia R-R:", arrayDistanciaPicos
print "Promedio de distancia R-R:", round(np.average(arrayDistanciaPicos), 3), "seg."  
    