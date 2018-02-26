import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    screen_res=app.desktop().screenGeometry()
    width,height=screen_res.width(),screen_res.height()

    window = QWidget()
    window.resize(300,300)
    window.move(0,0)
    window.setWindowTitle('Projet Anglais avec le point bonus')
    exitButton=QPushButton("Quitter",window)
    exitButton.clicked.connect(window.close)
    window.showFullScreen()
    
    sys.exit(app.exec_())