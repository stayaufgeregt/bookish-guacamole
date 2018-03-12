import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from listGuesserGUI import *

if __name__ == '__main__':
	
	
	app = QApplication(sys.argv)
	screen_res=app.desktop().screenGeometry()
	width,height=screen_res.width(),screen_res.height()

	launcher = QWidget()
	app1 = getWindowApp1(launcher)
	app2 = QWidget()
	
	
	def switch(window):
		launcher.hide()
		window.show()
		
	switch_app1=lambda : switch(app1)
	switch_app2=lambda : switch(app2)
	switch_laun=lambda : switch(launcher)
	
	#launcher window
	launcher.move(50,50)
	launcher.resize(300,300)
	launcher.setWindowTitle("Projet Anglais avec le point bonus")
	
	#exit button
	exitButton=QPushButton("Quitter",launcher)
	exitButton.clicked.connect(launcher.close)
	exitButton.move(32,32)
	
	
	#app1 button
	app1Button=QPushButton("Lancer app1",launcher)
	app1Button.clicked.connect(switch_app1)
	app1Button.move(32,160)
	
	#app2
	app2Button=QPushButton("Lancer app2",launcher)
	app2Button.clicked.connect(switch_app2)
	app2Button.move(32,288)
	
	launcher.show()
	
	sys.exit(app.exec_())