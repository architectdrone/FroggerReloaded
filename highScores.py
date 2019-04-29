#will store top 10 high scores to text file after game over
'''
scores_list = []#holds list of names and associated scores
class HighScores():   
    def __init__(self, name, score):
        '''
        @param name username
        @param score 
        '''
        '''
        self.name = name
        self.score = score
'''

    def addEntry(self, name, score):  
        '''
        '''
        adds entry to scores
        @param name username
        @param score 
        '''
        '''
        newEntry = {
            'name' : name,
            'score' : score
        }
        scores_list.append(newEntry)
'''

def readFromFileAndPrint(file_name):
        '''
        Reads entries from the score file and prints the entries
        @param file_name Name of file
        '''
	    file = open(file_name, 'r')
	    lines = file.readlines()
	    file.close

	    for line in lines:
	        entry = line.strip().split(",") #format in file will be name,score
	        print(entry[0] , entry[1]) #entry[0] is name, entry[1] is score
        
def writeToFile(file_name, name, score):
    '''
    Adds new entry to the file
    @param name Username to be added
    @param score User score to be added
    '''
    file = open(file_name, 'a')
	file.write(name + ',' + score)
	file.close()

def SortScores(file_name):
    '''
    Sorts all entries by score in the file and returns the entries as a list
    @param file_name 
    '''
    userScores_list = []
    file = open(file_name, 'r')
	lines = file.readlines()
    for line in lines:
        entry = line.strip().split(",")
        name = entry[0]
        score = int(entry[1])
        userScores_list.append(score, name)
        
    userScores_list.sort(reverse=True) #sort user scores descending order
    return userScores_list












    

