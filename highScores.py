#will store top 10 high scores to text file after game over


def readFromFileAndPrint(file_name):
    '''
    Reads entries from the score file and prints the entries
    @param file_name Name of file
    '''
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close

    for line in lines:
	    entry = line.split(",") #format in file will be name,score
	    print(entry[0] , entry[1]) #entry[0] is name, entry[1] is score
        
def writeToFile(file_name, name, score):
    '''
    Adds new entry to the file
    @param name Username to be added
    @param score User score to be added
    '''
    file = open(file_name, 'a')
    file.write("\n"+name + ',' + str(score))
    file.close()

def SortAndCompareScores(file_name, user_score):
    '''
    Sorts all entries by score in the file and returns True if user score is within top 10 scores
    @param file_name Name of score file
    @param user_score Score of the user 
    '''
    highScore = False
    userScores_list = []
    file = open(file_name, 'r')
    lines = file.readlines()
    for line in lines:
        entry = line.strip().split(",")
        score = int(entry[1])
        userScores_list.append(score)
        
    userScores_list.sort(reverse=True) #sort user scores descending order
    userScores_list = userScores_list[:10] #limit to top 10 entries

    for score in userScores_list:
        if user_score >= score:
            highScore = True
    
    return highScore













    

