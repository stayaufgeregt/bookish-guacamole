from PyQt5.QtWidgets import QApplication, QWidget, QPushButton



def getWindowApp1(launcher):
	
	window=QWidget()
	
	def switchBack():
		window.hide()
		launcher.show()
	
	window.move(400,300)
	window.resize(768,512)
	window.setWindowTitle("Application 1")
	
	#launcher button
	launcherButton=QPushButton("Back to main",window)
	launcherButton.clicked.connect(switchBack)
	launcherButton.move(32,32)
	
	return window