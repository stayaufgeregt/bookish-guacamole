from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from wordList import *
from listGuesser import *
import subprocess
import os

def getWindowApp(launcher):
	
	window=QWidget()
	
	def switchBack():
		window.hide()
		launcher.Show()
	
	
	def startGame():
		
		window=QWidget()
		vocabSheet=getVocabSheet()
		guess1word(vocabSheet)
		
		
	window.move(400,300)
	window.resize(768,512)
	window.setWindowTitle("Word Guesser")
	window.setStyleSheet("background-color:#debbee;")
	
	#launcher button
	launcherButton=QPushButton("Back to main",window)
	launcherButton.setStyleSheet("QPushButton{background-color:rgb(153, 204, 0);border-radius:10px;border:1px solid white;color:white;}")
	launcherButton.clicked.connect(switchBack)
	launcherButton.resize(128,48)
	launcherButton.move(608,448)
	
	#start game
	startButton=QPushButton("PLAY",window)
	startButton.setStyleSheet("QPushButton{background-color:rgb(153, 204, 0);font-size:48px;color:#fff;border-radius:10px;border:3px solid white;}")
	startButton.clicked.connect(startGame)
	startButton.resize(256,96)
	startButton.move(256,208)
	
	return window