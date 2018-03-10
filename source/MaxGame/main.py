import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout)


class Launcher(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):  

        #création des boutons
        ButtonProgression = QPushButton("Progression")
        ButtonMiniGame = QPushButton("Mini-jeu")
        ButtonProfil = QPushButton("Profil")

        #création des Hbox pour positionner les boutons

        vbox = QVBoxLayout()
        vbox.addStretch(1) #ajoute 1 espace avant les boutons
        vbox.addWidget(ButtonProgression)
        vbox.addWidget(ButtonMiniGame)
        vbox.addWidget(ButtonProfil)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)

        #création de la fenêtre
        self.setLayout(hbox)
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('English App')
        self.show() 

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Launcher()
    sys.exit(app.exec_())