import time

resources="../resources/"


def saveScore(points, playerName):
	#ajoute le score d'un joueur à une partie
	with open(resources+"score","a") as score:
	
		score.write(time.ctime()+"\t"+playerName+"\t"+str(points)+"\n")
		
	#
	
def getScoreBoard(**kwargs):
	#donne tous les scores (clé 'sort' pour trier)
	def parseLine(line):
		return tuple(line[:-1].split('\t'))
	
	scoreBoard=None
	with open(resources+"score",'r') as score:
		scoreBoard=list(map(parseLine,score.readlines()))
		
	
	if 'sort' in kwargs:
		return sortScoreBoard(scoreBoard,kwargs['sort'])
		
	return scoreBoard
	
def sortScoreBoard(scoreBoard,attribute):
	#trie un tableau de scores
	item_code={'date':0,'name':1,'point':2,'points':2}[attribute]
	
	if item_code==0:
		scoreBoard.sort(key=lambda x:time.strptime(x[0]), reverse=True)
	elif item_code==1:
		scoreBoard.sort(key=lambda x:x[1])
	elif item_code==2:
		scoreBoard.sort(key=lambda x:int(x[2]),reverse=True)
		
	return scoreBoard

if __name__=='__main__':
	
	saveScore(7,"Billy")
	saveScore(0,"Coco")
	saveScore(-14,"Refoulay")
		
		
	print(*getScoreBoard(sort='point'),sep='\n')