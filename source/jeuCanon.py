import sys
import math
import random
import time
import matplotlib as plt
import listGuesserGUI

from PyQt5.QtCore import (
    Qt,
    QBasicTimer,
    QSize
)
from PyQt5.QtGui import (
    QBrush,
    QTransform,
    QKeyEvent,
    QPixmap,
    QMovie,
    QIcon,
    QCursor
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsProxyWidget,
    QGraphicsScene,
    QGraphicsView
)
from PyQt5.QtMultimedia import(
    QSound
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
POSCanonX = 50
POSCanonY = 225
FRAME_TIME_MS = 20 #20ms/frame
VITESSECANON = 100 #metre/seconde
VITESSEPANIER = 20 #pix/sec
VITESSEPANIER2 = 50
VITESSEPANIER3 = 120
G = 25#9.81

#longueur 65 pixels
#hauteur 22 pixels

imagesFolder="../resources/images/"

class Scene(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)
        #les mots anglais
        self.Over =0
        self.MusicAmbiance = QSound("MusciFond.wav")
        self.MusicAmbiance.setLoops(-1)
        self.MusicAmbiance.play()
        self.Piece = QSound("piece.wav")
        self.motsMeeting = [["attend","assister à"],["miss","manquer"],["run/chair","s'occuper de"],["bring forward","avancer"],["set up/arrange","organiser"]]
        self.nbMot1 = random.randint(0,4)
        self.nbMot2 = random.randint(0,4)
        self.nbMot3 = random.randint(0,4)
        while self.nbMot2 == self.nbMot1 :
            self.nbMot2 = random.randint(0,4)
        while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
            self.nbMot3 = random.randint(0,4)
        self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
        
        self.motTargetFR = QGraphicsTextItem()
        self.motTargetFR.setPos(0,150)
        self.motTargetFR.setPlainText(self.motSelec[0][1])
        self.motTargetFR.setScale(2)

        self.motTargetEN1= QGraphicsTextItem()
        self.motTargetEN1.setPos(0,0)
        self.motTargetEN1.setPlainText(self.motSelec[0][0])
        self.motTargetEN1.setScale(2)

        self.motTargetEN2= QGraphicsTextItem()
        self.motTargetEN2.setPos(0,0)
        self.motTargetEN2.setPlainText(self.motSelec[1][0])
        self.motTargetEN2.setScale(2)

        self.motTargetEN3= QGraphicsTextItem()
        self.motTargetEN3.setPos(0,0)
        self.motTargetEN3.setPlainText(self.motSelec[2][0])
        self.motTargetEN3.setScale(2)

        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        self.tAnimation =0
        self.aniTrue = 0
        # hold the set of keys we're pressing
        self.keys_pressed = set()

        self.landscape = QGraphicsPixmapItem(QPixmap("landscape.png"))
        self.canon = QGraphicsPixmapItem(QPixmap("canon.png"))
        self.panier = QGraphicsPixmapItem(QPixmap("panier.png"))
        self.panier2 = QGraphicsPixmapItem(QPixmap("panier.png"))
        self.panier3 = QGraphicsPixmapItem(QPixmap("panier.png"))
        self.panier.setPos(300,300)
        self.canon.setTransformOriginPoint(15,47)
        self.panierSelec =random.randint(0,2)
        #zself.canon.setScale(2)

        self.boulet1 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet2 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet3 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet4 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet5 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet6 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet7 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet8 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.boulet9 = QGraphicsPixmapItem(QPixmap("boulet.png"))
        self.Coffre = []
        self.Coffre.append(self.boulet1)
        self.Coffre.append(self.boulet2)
        self.Coffre.append(self.boulet3)
        self.Coffre.append(self.boulet4)
        self.Coffre.append(self.boulet5)
        self.Coffre.append(self.boulet6)
        self.Coffre.append(self.boulet7)
        self.Coffre.append(self.boulet8)
        self.Coffre.append(self.boulet9)

        self.BouletLoupé=0

        self.music6 = QSound("pewpew.wav")

        self.canon.setRotation(-30)
        self.addItem(self.landscape)
        self.addItem(self.canon)
        self.addItem(self.panier)
        self.addItem(self.panier2)
        self.addItem(self.panier3)
        self.addItem(self.motTargetFR)
        self.addItem(self.motTargetEN1)
        self.addItem(self.motTargetEN2)
        self.addItem(self.motTargetEN3)

        self.zeta =0
        #le score
        self.score = QGraphicsTextItem()
        self.score.setPos(0,0)
        self.scoreNumber = 300##########################
        self.score.setPlainText("Score: "+str(self.scoreNumber))
        self.score.setScale(2)
        self.addItem(self.score)

        self.Niv = QGraphicsTextItem()
        self.Niv.setPos(370,0)
        self.niveau = 3##############################
        self.Niv.setPlainText("Level "+str(self.niveau))
        self.Niv.setScale(2)
        self.addItem(self.Niv)

        self.BoulLoup = QGraphicsTextItem()
        self.BoulLoup.setPos(300,200)
        self.BoulLoup.setPlainText("Tirs Loupés: "+str(self.BouletLoupé))
        self.BoulLoup.setScale(3)

        self.view = QGraphicsView(self)
        self.view.setGeometry(300, 300, 800, 400)
        self.view.setWindowTitle("Bookish-Quacamole")
        self.canon.setPos(POSCanonX,POSCanonY)
        self.view.show()
        self.setSceneRect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        
        self.listFIREOK=[0,0,0,0,0,0,0,0,0]
        self.cptBouletUsed =0
        self.listBoulet = [1,2,3,4,5,6,7,8,9]
        self.XBoulet=0
        self.YBoulet=0
        self.Coord = [self.XBoulet,self.YBoulet]
        self.listCoord = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        #print(self.listCoord)
        self.listeTemps =[0,0,0,0,0,0,0,0,0]
        self.listAlphaShot = [0,0,0,0,0,0,0,0,0]

        #Pour les Paniers
        self.CoorPanier = [190,300]
        self.tempsPanier = 0

        self.CoorPanier2 = [360,300]
        self.tempsPanier2 = 0

        self.CoorPanier3 = [540,300]
        self.tempsPanier3 = 0

        self.cptTour =0
        self.cptTour2 = 0
        self.MouseX = 0
        self.MouseY = 0

    def mouseMoveEvent(self,e):
        position = QCursor.pos()
        self.MouseX=position.x()
        self.MouseY=position.y()
        #print("X : ",self.MouseX,"Y : ",self.MouseY)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Z:
            self.canon.setRotation(self.canon.rotation()-2)
        if e.key() == Qt.Key_S:
            self.canon.setRotation(self.canon.rotation()+2)
            #print(-(math.fmod(self.canon.rotation(),360)-40))
        if e.key() == Qt.Key_Space:
            if(self.cptBouletUsed < 8):
                #print("FIRE!\n")
                self.music6.play()
                self.cptBouletUsed = self.cptBouletUsed+1
                self.listAlphaShot[self.listBoulet[0]-1] = (-(math.fmod(self.canon.rotation(),360)-40))*2*math.pi/360
                self.XBoulet=math.cos(self.listAlphaShot[self.listBoulet[0]-1])*50
                self.YBoulet=math.sin(self.listAlphaShot[self.listBoulet[0]-1])*50
                self.XBoulet = POSCanonX+15+self.XBoulet
                self.YBoulet = POSCanonY+47-self.YBoulet
                self.listFIREOK[self.listBoulet[0]-1]=1
                self.x =self.XBoulet
                self.y=self.YBoulet
                self.listCoord[self.listBoulet[0]-1][0]=self.XBoulet
                self.listCoord[self.listBoulet[0]-1][1]=self.YBoulet
                self.Coffre[self.listBoulet[0]-1].setPos(self.XBoulet,self.YBoulet)
                self.addItem(self.Coffre[self.listBoulet[0]-1])
                self.listBoulet = self.listBoulet[1:] #on enleve le boulet en bas de la liste
            else:
                #print("Plus de munition")
                pass

    def victoire(self):
        self.aniTrue=1
        self.label2 = QLabel()
        self.movie2 = QMovie("source.gif")
        self.wid2= QGraphicsProxyWidget()
        self.label2.setMovie(self.movie2)
        self.wid2.setWidget(self.label2)
        self.wid2.setPos(0,0)
        self.wid2.setScale(1)
        self.label2.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid2)
        self.movie2.start()
        
        self.label3 = QLabel()
        self.movie3 = QMovie("source.gif")
        self.wid3= QGraphicsProxyWidget()
        self.label3.setMovie(self.movie3)
        self.wid3.setWidget(self.label3)
        self.wid3.setPos(600,200)
        self.wid3.setScale(0.25)
        self.wid3.setRotation(-90)
        self.label3.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid3)
        self.movie3.start()

        self.label4 = QLabel()
        self.movie4 = QMovie("source.gif")
        self.wid4= QGraphicsProxyWidget()
        self.label4.setMovie(self.movie4)
        self.wid4.setWidget(self.label4)
        self.wid4.setPos(200,0)
        self.wid4.setScale(0.25)
        self.wid4.setRotation(90)
        self.label4.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid4)
        self.movie4.start()

        self.label = QLabel()
        self.movie = QMovie("wow.gif")
        self.wid = QGraphicsProxyWidget()
        self.label.setMovie(self.movie)
        self.wid.setWidget(self.label)
        self.wid.setPos(300,160)
        self.wid.setScale(1)
        self.label.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid)
        self.movie.start()
        self.music1 = QSound("wow.wav")
        self.music1.play()
        self.music2 = QSound("wowCOMBO.wav")
        self.music3 = QSound("Skrillex.wav")
        self.music4 = QSound("Triple.wav")
        self.music5 = QSound("airporn.wav")
        self.music2.play()
        self.music3.play()
        self.music4.play()
        self.music5.play()

    def victoireFinale(self):
        self.MusicAmbiance.stop()
        self.FinalMusic=QSound("monde-termine.wav")
        self.FinalMusic.play()

        self.label5 = QLabel()
        self.movie5 = QMovie("feu_artifice.gif")
        self.wid5= QGraphicsProxyWidget()
        self.label5.setMovie(self.movie5)
        self.wid5.setWidget(self.label5)
        self.wid5.setPos(300,50)
        self.wid5.setScale(0.25)
        self.wid5.setRotation(90)
        self.wid5.setScale(2)
        self.label5.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid5)
        self.movie5.start()

        self.label6 = QLabel()
        self.movie6 = QMovie("feu_artifice.gif")
        self.wid6= QGraphicsProxyWidget()
        self.label6.setMovie(self.movie6)
        self.wid6.setWidget(self.label6)
        self.wid6.setPos(700,50)
        self.wid6.setScale(0.25)
        self.wid6.setRotation(90)
        self.wid6.setScale(2)
        self.label6.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid6)
        self.movie6.start()

        self.BoulLoup.setPlainText("Tirs Loupés: "+str(self.BouletLoupé))
        self.addItem(self.BoulLoup)

        self.btnRetour = QPushButton("Menu")
        self.btnRetour.resize(200,52)
        self.btnRetour.clicked.connect(self.Retour)
        self.btnRetour.setAttribute(Qt.WA_TranslucentBackground)
        self.wid8 = QGraphicsProxyWidget()
        self.wid8.setWidget(self.btnRetour)  
        self.wid8.setPos(300,70)
        self.addItem(self.wid8)

    def Retour(self):
        self.view.hide()
        self.FinalMusic.stop()
        lanceur.Show()
        #sys.exit(app.exec_())


    def timerEvent(self, event):
        if self.Over == 0:
            #on oriente le canon
            if (self.MouseX-(15+POSCanonX+300)) != 0:
                self.zeta = math.atan((self.MouseY-(47+POSCanonY+200))/(self.MouseX-(15+POSCanonX+300)))
            self.zeta = (self.zeta*360)/(2*math.pi)
            self.canon.setRotation(self.zeta)
            self.update()
            #print("mot ",self.motSelec)
            #print("temps : ",self.tAnimation)
            if self.aniTrue ==1:
                self.tAnimation=self.tAnimation+FRAME_TIME_MS/200
                if self.tAnimation >16:
                    self.aniTrue=0
                    self.tAnimation=0
                    self.removeItem(self.wid2)
                    self.removeItem(self.wid3)
                    self.removeItem(self.wid4)
                    self.removeItem(self.wid)
                    self.music1.stop()
                    self.music2.stop()
                    self.music3.stop()
                    self.music4.stop()
                    self.music5.stop()

            if self.niveau == 1:    
                #print("cpt ",self.cptTour,"cpt2 ",self.cptTour2)
                if self.cptTour<50:
                    #print("ICI")
                    """
                    rand = random.randint(0,1)
                    rand2 = random.randint(0,1)
                    rand3 = random.randint(0,1) 
                    if rand == 0:
                        self.CoorPanier[0] = self.CoorPanier[0]+5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        
                    else:
                        self.CoorPanier[0] = self.CoorPanier[0]-5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        

                    if rand2 == 0:
                        self.CoorPanier2[0] = self.CoorPanier2[0]+5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        
                    else:
                        self.CoorPanier2[0] = self.CoorPanier2[0]-5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        

                    if rand3 == 0:
                        self.CoorPanier3[0] = self.CoorPanier3[0]+5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    else:
                        self.CoorPanier3[0] = self.CoorPanier3[0]-5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    """
                    
                    self.CoorPanier[0] = self.CoorPanier[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                    

                    self.CoorPanier2[0] = self.CoorPanier2[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)

                    self.update()
                    self.cptTour = self.cptTour+1
                if self.cptTour2<50 and self.cptTour>=50:
                    self.tempsPanier =0
                    self.CoorPanier[0] = self.CoorPanier[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                   

                    self.CoorPanier2[0] = self.CoorPanier2[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    
                    self.update()
                    self.cptTour2 = self.cptTour2+1

                if self.cptTour>=50 and self.cptTour2>=50:
                    self.cptTour=0
                    self.cptTour2=0
                u=0
                while u<9:
                    #print(u)
                    if self.listCoord[u][1] > 400: #ça sort de l'écran donc on annule le boulet
                        #print("OVER MAP !!!!!")
                        self.BouletLoupé=self.BouletLoupé+1
                        self.listFIREOK[u]=0
                        self.listCoord[u][0]=-20
                        self.listCoord[u][1]=-20
                        self.listeTemps[u] =0
                        self.listAlphaShot[u] = 0
                        self.cptBouletUsed= self.cptBouletUsed-1
                        self.listBoulet=self.listBoulet+[u+1]

                    if self.listCoord[u][0]>self.CoorPanier[0] and self.listCoord[u][0]<(self.CoorPanier[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier[1] and self.listCoord[u][1]<(self.CoorPanier[1]+50) and self.panierSelec==0:
                            self.Piece.play()
                            if self.scoreNumber <200 and self.scoreNumber>=100:
                                self.niveau = 2
                                self.victoire()

                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier2[0] and self.listCoord[u][0]<(self.CoorPanier2[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier2[1] and self.listCoord[u][1]<(self.CoorPanier2[1]+50) and self.panierSelec==1:
                            self.Piece.play()
                            if self.scoreNumber <200 and self.scoreNumber>=100:
                                self.niveau = 2
                                self.victoire()

                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier3[0] and self.listCoord[u][0]<(self.CoorPanier3[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier3[1] and self.listCoord[u][1]<(self.CoorPanier3[1]+50) and self.panierSelec==2:
                            self.Piece.play()
                            if self.scoreNumber <200 and self.scoreNumber>=100:
                                self.niveau = 2
                                self.victoire()
                            
                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]
                        

                    if self.listFIREOK[u] == 1:
                        self.listCoord[u][0] = self.x+math.cos(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.listCoord[u][1] = self.y+(0.5)*G*self.listeTemps[u]*self.listeTemps[u]-math.sin(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.Coffre[u].setPos(self.listCoord[u][0],self.listCoord[u][1])
                        self.update()
                        self.listeTemps[u]=self.listeTemps[u]+FRAME_TIME_MS/200

                    u=u+1
                    #print("/////////////////////")
            if self.niveau ==2:
                if self.cptTour<50:
                    """
                    rand = random.randint(0,1)
                    rand2 = random.randint(0,1)
                    rand3 = random.randint(0,1) 
                    if rand == 0:
                        self.CoorPanier[0] = self.CoorPanier[0]+5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        
                    else:
                        self.CoorPanier[0] = self.CoorPanier[0]-5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        

                    if rand2 == 0:
                        self.CoorPanier2[0] = self.CoorPanier2[0]+5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        
                    else:
                        self.CoorPanier2[0] = self.CoorPanier2[0]-5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        

                    if rand3 == 0:
                        self.CoorPanier3[0] = self.CoorPanier3[0]+5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    else:
                        self.CoorPanier3[0] = self.CoorPanier3[0]-5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    """
                    
                    self.CoorPanier[0] = self.CoorPanier[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                    

                    self.CoorPanier2[0] = self.CoorPanier2[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)

                    self.update()
                    self.cptTour = self.cptTour+1
                if self.cptTour2<50 and self.cptTour>=50:
                    self.tempsPanier =0
                    self.CoorPanier[0] = self.CoorPanier[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                   

                    self.CoorPanier2[0] = self.CoorPanier2[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    
                    self.update()
                    self.cptTour2 = self.cptTour2+1

                if self.cptTour>=50 and self.cptTour2>=50:
                    self.cptTour=0
                    self.cptTour2=0
                u=0
                while u<9:
                    #print(u)
                    if self.listCoord[u][1] > 400: #ça sort de l'écran donc on annule le boulet
                        #print("OVER MAP !!!!!")
                        self.BouletLoupé=self.BouletLoupé+1
                        self.listFIREOK[u]=0
                        self.listCoord[u][0]=-20
                        self.listCoord[u][1]=-20
                        self.listeTemps[u] =0
                        self.listAlphaShot[u] = 0
                        self.cptBouletUsed= self.cptBouletUsed-1
                        self.listBoulet=self.listBoulet+[u+1]

                    if self.listCoord[u][0]>self.CoorPanier[0] and self.listCoord[u][0]<(self.CoorPanier[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier[1] and self.listCoord[u][1]<(self.CoorPanier[1]+50) and self.panierSelec==0:
                            self.Piece.play()
                                
                            if self.scoreNumber <300 and self.scoreNumber>=200:
                                self.niveau = 3
                                self.victoire()

                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier2[0] and self.listCoord[u][0]<(self.CoorPanier2[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier2[1] and self.listCoord[u][1]<(self.CoorPanier2[1]+50) and self.panierSelec==1:
                            self.Piece.play()
                            if self.scoreNumber <300 and self.scoreNumber>=200:
                                self.niveau = 3
                                self.victoire()

                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier3[0] and self.listCoord[u][0]<(self.CoorPanier3[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier3[1] and self.listCoord[u][1]<(self.CoorPanier3[1]+50) and self.panierSelec==2:
                            self.Piece.play()
                            if self.scoreNumber <300 and self.scoreNumber>=200:
                                self.niveau = 3
                                self.victoire()
                            
                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]
                        

                    if self.listFIREOK[u] == 1:
                        self.listCoord[u][0] = self.x+math.cos(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.listCoord[u][1] = self.y+(0.5)*G*self.listeTemps[u]*self.listeTemps[u]-math.sin(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.Coffre[u].setPos(self.listCoord[u][0],self.listCoord[u][1])
                        self.update()
                        self.listeTemps[u]=self.listeTemps[u]+FRAME_TIME_MS/200

                    u=u+1
            if self.niveau ==3:
                if self.cptTour<50:
                    """
                    rand = random.randint(0,1)
                    rand2 = random.randint(0,1)
                    rand3 = random.randint(0,1) 
                    if rand == 0:
                        self.CoorPanier[0] = self.CoorPanier[0]+5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        
                    else:
                        self.CoorPanier[0] = self.CoorPanier[0]-5
                        self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                        

                    if rand2 == 0:
                        self.CoorPanier2[0] = self.CoorPanier2[0]+5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        
                    else:
                        self.CoorPanier2[0] = self.CoorPanier2[0]-5
                        self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                        

                    if rand3 == 0:
                        self.CoorPanier3[0] = self.CoorPanier3[0]+5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    else:
                        self.CoorPanier3[0] = self.CoorPanier3[0]-5
                        self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])
                        
                    """
                    
                    self.CoorPanier[0] = self.CoorPanier[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                    

                    self.CoorPanier2[0] = self.CoorPanier2[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]+VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)

                    self.update()
                    self.cptTour = self.cptTour+1
                if self.cptTour2<50 and self.cptTour>=50:
                    self.tempsPanier =0
                    self.CoorPanier[0] = self.CoorPanier[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier = self.tempsPanier+FRAME_TIME_MS/200
                    self.panier.setPos(self.CoorPanier[0],self.CoorPanier[1])
                   

                    self.CoorPanier2[0] = self.CoorPanier2[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier2 = self.tempsPanier2+FRAME_TIME_MS/200
                    self.panier2.setPos(self.CoorPanier2[0],self.CoorPanier2[1])
                    

                    self.CoorPanier3[0] = self.CoorPanier3[0]-VITESSEPANIER2*(FRAME_TIME_MS/200)
                    self.tempsPanier3 = self.tempsPanier3+FRAME_TIME_MS/200
                    self.panier3.setPos(self.CoorPanier3[0],self.CoorPanier3[1])

                    if self.panierSelec == 0:
                        self.motTargetEN1.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 1:
                        self.motTargetEN2.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN3.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    if self.panierSelec == 2:
                        self.motTargetEN3.setPos(self.CoorPanier[0]-10,self.CoorPanier[1]+60)
                        self.motTargetEN2.setPos(self.CoorPanier2[0]-10,self.CoorPanier2[1]+60)
                        self.motTargetEN1.setPos(self.CoorPanier3[0]-10,self.CoorPanier3[1]+60)
                    
                    self.update()
                    self.cptTour2 = self.cptTour2+1

                if self.cptTour>=50 and self.cptTour2>=50:
                    self.cptTour=0
                    self.cptTour2=0
                u=0
                while u<9:
                    #print(u)
                    if self.listCoord[u][1] > 400: #ça sort de l'écran donc on annule le boulet
                        #print("OVER MAP !!!!!")
                        self.BouletLoupé=self.BouletLoupé+1
                        self.listFIREOK[u]=0
                        self.listCoord[u][0]=-20
                        self.listCoord[u][1]=-20
                        self.listeTemps[u] =0
                        self.listAlphaShot[u] = 0
                        self.cptBouletUsed= self.cptBouletUsed-1
                        self.listBoulet=self.listBoulet+[u+1]

                    if self.listCoord[u][0]>self.CoorPanier[0] and self.listCoord[u][0]<(self.CoorPanier[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier[1] and self.listCoord[u][1]<(self.CoorPanier[1]+50) and self.panierSelec==0:
                            self.Piece.play()
                                
                            if self.scoreNumber == 300 :
                                self.victoireFinale()
                                self.Over=1

                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier2[0] and self.listCoord[u][0]<(self.CoorPanier2[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier2[1] and self.listCoord[u][1]<(self.CoorPanier2[1]+50) and self.panierSelec==1:
                            self.Piece.play()
                            if self.scoreNumber == 300:
                                self.victoireFinale()
                                self.Over=1
                                
                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]

                    if self.listCoord[u][0]>self.CoorPanier3[0] and self.listCoord[u][0]<(self.CoorPanier3[0]+50):
                        if self.listCoord[u][1]>self.CoorPanier3[1] and self.listCoord[u][1]<(self.CoorPanier3[1]+50) and self.panierSelec==2:
                            self.Piece.play()
                            if self.scoreNumber == 300:
                                self.victoireFinale()
                                self.Over=1
                            
                            self.panierSelec = random.randint(0,2)
                            motTemp = self.nbMot1
                            self.nbMot1 = random.randint(0,4)
                            self.nbMot2 = random.randint(0,4)
                            self.nbMot3 = random.randint(0,4)
                            while self.nbMot1 == motTemp:
                                self.nbMot1 = random.randint(0,4)
                            while self.nbMot2 == self.nbMot1 :
                                self.nbMot2 = random.randint(0,4)
                            while self.nbMot3 == self.nbMot2 or self.nbMot3 == self.nbMot1 :
                                self.nbMot3 = random.randint(0,4)
                            self.motSelec = [self.motsMeeting[self.nbMot1],self.motsMeeting[self.nbMot2],self.motsMeeting[self.nbMot3]]
                            self.motTargetFR.setPlainText(self.motSelec[0][1])
                            self.motTargetEN1.setPlainText(self.motSelec[0][0])
                            self.motTargetEN2.setPlainText(self.motSelec[1][0])
                            self.motTargetEN3.setPlainText(self.motSelec[2][0])
                            self.Niv.setPlainText("Level "+str(self.niveau))
                            self.scoreNumber = self.scoreNumber+10
                            self.score.setPlainText("Score: "+str(self.scoreNumber))
                            self.update()
                            y =0
                            while(y<9):
                                self.listFIREOK[y]=0
                                self.listCoord[y][0]=-20
                                self.listCoord[y][1]=-20
                                self.listeTemps[y] =0
                                self.listAlphaShot[y] = 0
                                self.Coffre[y].setPos(self.listCoord[y][0],self.listCoord[y][1])
                                y=y+1
                            
                            self.cptBouletUsed= 0
                            self.listBoulet=[1,2,3,4,5,6,7,8,9]
                        

                    if self.listFIREOK[u] == 1:
                        self.listCoord[u][0] = self.x+math.cos(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.listCoord[u][1] = self.y+(0.5)*G*self.listeTemps[u]*self.listeTemps[u]-math.sin(self.listAlphaShot[u])*VITESSECANON*self.listeTemps[u]
                        self.Coffre[u].setPos(self.listCoord[u][0],self.listCoord[u][1])
                        self.update()
                        self.listeTemps[u]=self.listeTemps[u]+FRAME_TIME_MS/200

                    u=u+1

class Launcher(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)
        self.jeu2=listGuesserGUI.getWindowApp(self)
        self.initUI()
        

    def initUI(self):
        
        self.view = QGraphicsView(self)
        self.view.setGeometry(300, 300, 960, 540)
        self.view.setWindowTitle("Bookish-Quacamole")
        self.setSceneRect(0,0,960,540)
        
        self.btn = QPushButton()
        self.btn.setStyleSheet("QPushButton{background-color:transparent;border-image:url(buttonGame1.png);background:none;border:none;}")
        self.btn.resize(200,52)
        self.btn.clicked.connect(self.Jeu1)
        self.btn.setAttribute(Qt.WA_TranslucentBackground)
        self.wid1 = QGraphicsProxyWidget()
        self.wid1.setWidget(self.btn)  
        self.wid1.setPos(380,265)

        self.btn2 = QPushButton()
        self.btn2.setStyleSheet("QPushButton{background-color:transparent;border-image:url(buttonGame2.png);background:none;border:none;}")
        self.btn2.resize(200,52)
        self.btn2.clicked.connect(self.Jeu2)
        self.btn2.setAttribute(Qt.WA_TranslucentBackground)
        self.wid2 = QGraphicsProxyWidget()
        self.wid2.setWidget(self.btn2)  
        self.wid2.setPos(380,337) 
    
        self.btn3 = QPushButton()
        self.btn3.setStyleSheet("QPushButton{background-color:transparent;border-image:url(buttonProgress.png);background:none;border:none;}")
        self.btn3.resize(200,52)
        self.btn3.clicked.connect(self.Progress)
        self.btn3.setAttribute(Qt.WA_TranslucentBackground)
        self.wid3 = QGraphicsProxyWidget()
        self.wid3.setWidget(self.btn3)  
        self.wid3.setPos(380,409)

        self.MusicAmbiance = QSound("Launcher.wav")
        self.MusicAmbiance.setLoops(-1)
        self.MusicAmbiance.play()

        self.label5 = QLabel()
        self.movie5 = QMovie("Particule.gif")
        self.wid5= QGraphicsProxyWidget()
        self.label5.setMovie(self.movie5)
        self.wid5.setWidget(self.label5)
        self.wid5.setScale(0.5)
        self.label5.setAttribute(Qt.WA_NoSystemBackground)
        self.addItem(self.wid5)
        self.movie5.start()
        self.addItem(self.wid1)
        self.addItem(self.wid2)
        self.addItem(self.wid3)

        self.view.show()
    
    def Jeu1(self):
        #print("Jeu 1")
        self.view.hide()
        self.MusicAmbiance.stop()
        scene = Scene(self)

    def Jeu2(self):
        #print("Jeu 2")
        self.view.hide()
        self.MusicAmbiance.stop()
        self.jeu2.show()
        
        

    def Progress(self):
        #print("Progress")
        pass
    def Show(self):
        self.view.show()
        self.MusicAmbiance.play()

class ProgressScene(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)
        self.initUI()
    def initUI(self):
       
        self.view = QGraphicsView(self)
        self.view.setGeometry(300, 300, 960, 540)
        self.view.setWindowTitle("Bookish-Quacamole")
        self.setSceneRect(0,0,960,540)
        
        self.btn = QPushButton()
        self.btn.setStyleSheet("QPushButton{background-color:transparent;border-image:url(buttonGame1.png);background:none;border:none;}")
        self.btn.resize(200,52)
        self.btn.clicked.connect(self.Menu)
        self.btn.setAttribute(Qt.WA_TranslucentBackground)
        self.wid1 = QGraphicsProxyWidget()
        self.wid1.setWidget(self.btn)
        self.wid1.setPos(380,265)

        self.addItem(self.wid1)

        self.view.show()
    
    def Menu(self):
        #print("Jeu 1")
        pass


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(imagesFolder+"avocado.ico"))
    lanceur = Launcher()
    sys.exit(app.exec_())