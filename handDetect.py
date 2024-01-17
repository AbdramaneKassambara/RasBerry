# import les biblioteque
import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import requests
# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()
# Configuration des propriétés du moteur (facultatif)
engine.setProperty('rate', 250)  # Vitesse de la voix (mots par minute)
engine.setProperty('volume', 1.0)  # Volume de la voix (de 0.0 à 1.0)
# initialisation de la camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
#init detect
detector = HandDetector(maxHands=2,detectionCon=0.8)
url = "http://192.168.1.25:5000/"
headers = {"Content-Type": "application/json"}

while True:
    success, img = camera.read()
    # dectect la main 
    hands,img = detector.findHands(img,True)
    # Vérifier s'il y a des mains détectées
    handType =None
    text_to_speak =None
    if hands:
        for hand in hands:

            main = hands[0]
            doigt = detector.fingersUp(main)
            nombre_doigts = doigt.count(1)
            data = {"nombre_doigts": nombre_doigts} 
            response = requests.post(url, json=data, headers=headers)
            #print (nombre_doits)
            if hand["type"] == "Right":
                text_to_speak = "Main droite détectée"
                handType = "Droite"
                
            else:
                text_to_speak = "Main gauche détectée"
                handType = "Gauche"  
            if (len(hands))==2:
                text = f" 2 Mains {nombre_doigts} doigts"
                text_to_speak = " 2 Main détectée"
            else :
                text = f" Main {handType} {nombre_doigts} doigts "
            origine = (200, 100)
            fontFace = cv2.FONT_ITALIC
            fontScale = 3
            color = (0, 255, 0)  # Vert en BGR
            thickness = 2
            lineType = cv2.LINE_AA
           # cv2.putText(img, text, origine, fontFace, fontScale, color, thickness, lineType)
            #engine.say(text_to_speak)
            #engine.runAndWait()
    # Affiche de l'image avec le dectect main 
    cv2.imshow("Dectection des main",img)
    # Pour quitter la boucle lorsque la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)
# Libération des ressources et fermeture de la fenêtre
camera.release()
cv2.destroyAllWindows()