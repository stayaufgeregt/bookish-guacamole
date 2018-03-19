from PyQt5.QtWidgets import QFileDialog
import json
import os

vocabFolder="../resources/vocabulary/"

def secureInput(inputText,errorMessage="",**kwargs):
	
	result=input(inputText)
	
	if "blackList" in kwargs:
		while result in kwargs["blackList"]:
			print(errorMessage)
			result=input(inputText)
	elif "whiteList" in kwargs:
		while not(result in kwargs["whiteList"]):
			print(errorMessage)
			result=input(inputText)
		
	return result
	
	
def createVocabSheet():

	listName=input("Enter sheet name (case sensitive): ")
	listPath=vocabFolder+listName+".li"
	vocabSheet={}
	
	#if file already exists, load its content beforehand
	if os.path.isfile(listPath):
		with open(listPath,"r") as vocabList:
			vocabSheet=json.load(vocabList)
		#
	
	
	with open(listPath,"w") as vocabList:
		
		frenchWord=secureInput("French word : ")
		
		while not(frenchWord in ["","quit","q","exit"]):
		
			englishTranslation=secureInput("English translation of "+frenchWord+" : ","Word needs to be non null",blackList=["",None])
			vocabSheet[frenchWord]=englishTranslation
			frenchWord=secureInput("French word : ")
		
		json.dump(vocabSheet,vocabList)
		
	print("Sheet saved")
	
	
def getVocabSheet():
	"""vocabLists=[fileName[:-3] for fileName in os.listdir(vocabFolder) if len(fileName)>3 and fileName[-3:]==".li" ]
	vocabSheet=None
	
	if len(vocabLists)==0:
		print("No vocabulary lists available, create some !")
		return
		
	print(*vocabLists,sep="\n")
	listName=secureInput("Choose the list you want to train : ","you must pick one of the following lists : \n"+"\n".join(vocabLists),whiteList=vocabLists)
	"""
	
	vocabSheet=None
	listPath=QFileDialog.getOpenFileName(None,"Choose a training list",vocabFolder,"vocab list (*.li)")[0]
	
	with open(listPath,"r") as vocabFile:
		vocabSheet=json.load(vocabFile)
		
	return vocabSheet
	
if __name__=='__main__':
	createVocabSheet()
	print(*[key+" : "+value for key,value in getVocabSheet().items()],sep="\n")
	