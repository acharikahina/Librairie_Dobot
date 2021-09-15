import threading
import DobotLib as lib


lib.connecter()

while(True):
    lib.Convoyeur1()
    while(True):
        vrai=lib.objet1()
        while(vrai==0):
            vrai=lib.objet1()
        if(vrai):
            lib.pause(570) #Ne pas changer
            lib.ArretConvoyeur1()
            lib.prise()
            lib.pause(1000)
            couleur = lib.getColor1()

            if(couleur==0):
                lib.pause(500)
                lib.triRed()
            if(couleur==1):
                lib.pause(500)
                lib.triGreen()
            if(couleur==2):
                lib.pause(500)
                lib.triBlue()
            break
        break
    lib.pause(2000)
    
# lib.Alarms()
# lib.Home()

# lib.Convoyeur1()
# lib.pause(5000)
# lib.ArretConvoyeur1()

# lib.Convoyeur2()
# lib.pause(5000)
# lib.ArretConvoyeur2()

# lib.objet1()

# lib.prise()
# lib.pinceOn()
# lib.pause()
# lib.pinceOff()
# lib.pause()
# lib.initPince()
# lib.triRed()
# lib.triGreen()
# lib.triBlue()
# while(1):
    # lib.getColor1()
lib.arretTotal()
lib.deconnecter

    




