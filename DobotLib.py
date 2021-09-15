"""Cette lib permet d'utiliser le bras robotique pour des TP de AED"""

from ctypes import *
import time,  platform
import os
import math
import sys
import DobotDllType as dType  # Librairie du constructeur

api = dType.load()

# Variable global permettant de onnaitre l'etat d'execution de la fonction prise
FIN_PRISE = 0

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}


def connecter():
    #Connection au Dobot
    state = dType.ConnectDobot(api, "COM3", 115200)[0] #
    print("Connect status:",CON_STR[state])
 
 
def arretTotal():
    initPince()
    ArretConvoyeur1()
    dType.SetInfraredSensor(api,0,2,1)
    startQueue()
    stopQueue()
    dType.SetColorSensor(api, 0, 1, 1)
    startQueue()
    stopQueue()
    
def deconnecter():
    ArretConvoyeur1()
    dType.SetInfraredSensor(api,0,port,1)
    startQueue()
    stopQueue()
    dType.SetColorSensor(api, 0, 1, 1)
    startQueue()
    stopQueue()
    pause(1000)
    #Disconnect Dobot
    dType.DisconnectDobot(api)
       
def startQueue():
    #Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    #while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
    #dType.dSleep(1000)
    
def stopQueue():
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api) 

def pause(duree=2000): 
    #Temps en millisecondes
    dType.dSleep(int(duree))


DELAY=1000

priseX=274
priseY=-154.8
priseZ=85
priseR=67

triRedX=77
triRedY=282
triRedZ=100
triRedR=160

triGreenX=-60
triGreenY=300
triGreenZ=100
triGreenR=160

triBlueX=-69
triBlueY=-273
triBlueZ=53
triBlueR=-9

#initialisation des param

def Config():
    VEL=200
    ACC=200
    dType.SetHOMEParams(api,250,  0,  80,  100,  isQueued=1)
    dType.SetPTPJointParams(api,VEL,ACC,VEL,ACC,VEL,ACC,VEL,ACC,isQueued = 1)
    dType.SetPTPCoordinateParams(api,VEL,ACC,VEL,ACC,isQueued = 1)
    dType.SetPTPJumpParams(api, 10, 200,isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100,isQueued = 1)
    #colour
    dType.SetColorSensor(api, 1, 1, 1)
    startQueue()
    stopQueue()
    
    
def Home():
    dType.SetHOMECmd(api,1000, isQueued=1)
    startQueue()
    dType.dSleep(30000)
    stopQueue()

def Alarms():
    al=dType.GetAlarmsState(api,1000)
    print(al)
    final=dType.ClearAllAlarmsState(api)
    print(final)
    startQueue()
    stopQueue()
    
#les fonctions

def pinceOn():
    ON=0
    OFF=1
    dType.SetEndEffectorParams(api, 80, 0, 0, 1)# Ne pas changer 80,0,0
    startQueue()
    stopQueue()
    dType.SetEndEffectorGripper(api, 1,  ON, 1)
    startQueue()
    dType.dSleep(2000)
    stopQueue()
    dType.SetEndEffectorGripper(api, 0,  OFF, 1)
    startQueue()
    dType.dSleep(100)
    stopQueue()
   
    
    
def pinceOff():
    ON=0
    OFF=1
    dType.SetEndEffectorParams(api, 80, 0, 0, 1)
    dType.SetEndEffectorGripper(api, 1,  OFF, 1) #1 ==enable
    startQueue()
    dType.dSleep(90)
    stopQueue()
    dType.SetEndEffectorGripper(api, 0,  OFF, 1)
    startQueue()
    stopQueue()

  


def initPince():
    ON=0
    OFF=1
    dType.SetEndEffectorParams(api, 80, 0, 0, 1)
    dType.SetEndEffectorGripper(api, 1,  OFF, 1) #1 ==enable moteur
    startQueue()
    dType.dSleep(500)
    stopQueue()
    dType.SetEndEffectorGripper(api, 0,  OFF, 1)
    startQueue()
    stopQueue()

def prise():
	FIN_PRISE = 0
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, priseX, priseY,priseZ,priseR,1)[0]
    dType.dSleep(1000)
    pinceOn()
    dType.dSleep(1000)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, priseX, priseY, 50,priseR,1)[0]
    startQueue()
    dType.dSleep(1000)
    stopQueue()
    pinceOff()
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, priseX, priseY, priseZ,priseR,1)[0]
    startQueue()
    stopQueue()
    FIN_PRISE =1
    return 1
    
    
def fin_prise():
    etat_de_prise = FIN_PRISE # On recupere l'etat de prise
    FIN_PRISE = 0 #RàZ de FIN_PRISE
    return etat_de_prise


def triRed():
    dType.dSleep(100)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, triRedX, triRedY, triRedZ,triRedR,1)[0]
    startQueue()
    dType.dSleep(2000)
    stopQueue()
    pinceOn()
    dType.dSleep(100)
    initPince() # init a la fin de prise
    return 1




def triGreen():
    dType.dSleep(100)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, triGreenX, triGreenY, triGreenZ,triGreenR,1)[0]
    startQueue()
    dType.dSleep(2000)
    stopQueue()
    pinceOn()
    dType.dSleep(100)
    initPince() # init a la fin de prise
    return 1

    
    
def triBlue():
    dType.dSleep(100)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, triBlueX, triBlueY, triBlueZ,triBlueR,1)[0]
    startQueue()
    dType.dSleep(2000)
    stopQueue()
    pinceOn()
    dType.dSleep(100)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, triBlueX, triBlueY, triBlueZ+50,triBlueR,1)[0]
    startQueue()
    dType.dSleep(500)
    stopQueue()
    initPince() # init a la fin de prise
    return 1

    



def Convoyeur1():
    # ID_INFRARED_SENSOR=2
    # dType.SetInfraredSensor(api,  1, 2, 1)

    STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0 # Pas par cycle
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
    # print("Vitesse du convoyeur: ")
    # print(vel)
    dType.SetEMotor(api, 0,1, int(vel), 1)
    startQueue()
    stopQueue()


def ArretConvoyeur1():
    STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0 # Pas par cycle
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
    # print("Vitesse du convoyeur: ")
    # print(vel)
    dType.SetEMotor(api, 0,0, 0, 1)
    startQueue()
    stopQueue() 
    

def Convoyeur2():
    STEP_PER_CRICLE = -360.0 / 1.8 * 10.0 * 16.0 # Pas par cycle
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
    # print("Vitesse du convoyeur: ")
    # print(vel)
    dType.SetEMotor(api, 1,1, int(vel), 1)
    startQueue()
    stopQueue()
 
 
def ArretConvoyeur2():
    STEP_PER_CRICLE = -360.0 / 1.8 * 10.0 * 16.0 # Pas par cycle
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
    # print("Vitesse du convoyeur: ")
    # print(vel)
    dType.SetEMotor(api, 1,0, int(vel), 1)
    startQueue()
    stopQueue()        
 

def color(colorPort=1,version=1):
    dType.SetColorSensor(api, 1, colorPort, version)
    startQueue()
    stopQueue()
    dType.dSleep(1000)
    colors=dType.GetColorSensor(api)
    startQueue()
    stopQueue()
    if(colors[0]== 1):
        print("ROUGE")
        #dType.SetColorSensor(api, 0, colorPort, version)
        startQueue()
        stopQueue()
        return 0
    if(colors[1]== 1):
        print("VERT")
        #dType.SetColorSensor(api, 0, colorPort, version)
        startQueue()
        stopQueue()
        return 1
    if(colors[2]== 1):
        print("BLUE")
        #dType.SetColorSensor(api, 0,colorPort, version)
        startQueue()
        stopQueue()
        return 2
            
            
def getColor1():
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, priseX-83, priseY, 58,priseR,1)
    startQueue()
    dType.dSleep(1000)
    stopQueue()
    col = color()
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, priseX-83, priseY, priseZ,priseR,1)
    startQueue()
    dType.dSleep(DELAY)
    stopQueue()
    return col

def objet1(id_sensor=2,port=2):
    dType.SetInfraredSensor(api,1,port,1)
    objetPresent=dType.GetInfraredSensor(api, id_sensor)
    startQueue()
    stopQueue()
    #print(objetPresent)
    return objetPresent[0]
    
def getPosition():
    pos=dType.GetPose(api)
    position=[0,0,0,0]
    position[0]=round(pos[0],2)
    position[1]=round(pos[1],2)
    position[2]=round(pos[2],2)
    position[3]=round(pos[3],2)
    return position
