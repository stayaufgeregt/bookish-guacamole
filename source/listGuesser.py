from wordList import *
from difflib import SequenceMatcher as match
import time
import random

def normalize(word):
	return str.lower(" ".join(word.split()))

def similitude(word1, word2):
	return match(None,word1,word2).ratio()
	
def guess1word(vocabSheet):
	
	print("Traduisez les mots suivants !")
	
	score=0
	closeWords=0
	start=time.time()
	
	words=list(vocabSheet.items())
	random.shuffle(words)
	for keyWord,wordToGuess in words:
		answer=normalize(secureInput(keyWord+" : ","Answer cannot be empty !",blackList=[""]))
		
		rightness=similitude(wordToGuess,answer)
		if rightness==1:
			print("Nice +1 !")
			score+=1
		elif 0.85<=rightness:
			print("Close, it was : "+wordToGuess)
			closeWords+=0.5
		elif 0.7<=rightness:
			print("Come on, you can do better : "+wordToGuess)
			closeWords+=0.25
		else:
			print("Wrong, it was : "+wordToGuess)
		
	
	spentTime=time.time()-start
	print("You guessed {}/{} words in {} seconds !".format(score,len(vocabSheet),spentTime))
	
	return int((1000*score+100*closeWords)/spentTime)
	
	
if __name__=='__main__':
	
	print(guess1word(getVocabSheet()))