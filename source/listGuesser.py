from wordList import *
import time
import random

	

def guess1word(vocabSheet):
	
	print("Traduisez les mots suivants !")
	
	score=0
	start=time.time()
	
	words=list(vocabSheet.items())
	random.shuffle(words)
	for keyWord,wordToGuess in words:
		answer=secureInput(keyWord+" : ","Answer cannot be empty !",blackList=[""])
		
		if wordToGuess==answer:
			print("Nice !")
			score+=1
		else:
			print("Wrong, it was : "+wordToGuess)
		
	
	spentTime=time.time()-start
	print("You guessed {}/{} words in {} seconds !".format(score,len(vocabSheet),spentTime))
	
	return int(1000*score/spentTime)
	
	
if __name__=='__main__':
	
	print(guess1word(getVocabSheet()))