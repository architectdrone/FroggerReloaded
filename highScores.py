#will store high scores to text file after game over


def findHighestScore(file_name):
    '''
    Reads entries from the score file and returns highest score
    @param file_name Name of file
    '''
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close

    highest_score = 0

    if len(lines) > 0:
        for line in lines:
            entry = line.strip().split(",") #format in file will be name,score so name=entry[0] and score=entry[1]
            #print(entry[0] , entry[1]) #entry[0] is name, entry[1] is score
            score = int(entry[1])
            if score > highest_score:
                highest_score = score

    return highest_score

        
def writeToFile(file_name, name, score):
    '''
    Adds new entry to the file
    @param name Username to be added
    @param score User score to be added
    '''
    file = open(file_name, 'a')
    file.write(name + ',' + str(score)+"\n")
    file.close()


def displayScores(file_name, n_entries):
    '''
    Displays n number of users and score by descending order
    @param file_name Name of file
    @param n_entries Number of entries
    '''
    userScores_list = []
    file = open(file_name, 'r')
    lines = file.readlines()
    
    for line in lines:
        entry = line.strip().split(",")
        name = entry[0]
        score = int(entry[1])
        userScores_list.append((score, name))
        
    userScores_list.sort(reverse=True) #sort user scores descending order
    if len(lines) < n_entries:
        n_entries = len(lines)
    userScores_list = userScores_list[:n_entries] #limit to n number of entries
    userScores_list = [entries[::-1] for entries in userScores_list] #name,score format instead of score,name
    print("Top scores:")
    print("Name Score" + '\n')
    for entry in userScores_list:
        print(entry[0] + " "+ str(entry[1]))

def getScores(file_name, n_entries):
    '''
    Gets n number of users and score by descending order
    @param file_name Name of file
    @param n_entries Number of entries
    @return a list of entries. The entries are formatted as tuples, like so: (name, score)
    '''
    userScores_list = []
    file = open(file_name, 'r')
    lines = file.readlines()
    
    for line in lines:
        entry = line.strip().split(",")
        name = entry[0]
        score = int(entry[1])
        userScores_list.append((score, name))
        
    userScores_list.sort(reverse=True) #sort user scores descending order
    if len(lines) < n_entries:
        n_entries = len(lines)
    userScores_list = userScores_list[:n_entries] #limit to n number of entries
    userScores_list = [entries[::-1] for entries in userScores_list] #name,score format instead of score,name

    toReturn = []
    for entry in userScores_list:
        toReturn.append((entry[0],entry[1]))

filename = "highscores.txt"
'''
writeToFile(filename, "Owen", 34)
writeToFile(filename,"Gwen", 78)
writeToFile(filename, "Jack", 12)
writeToFile(filename, "Steve", 41)
writeToFile(filename, "Bob", 13)
writeToFile(filename, "Jack", 2)
writeToFile(filename, "Jack", 5)
writeToFile(filename, "Jack", 2)
writeToFile(filename, "Jack", 89)
writeToFile(filename, "Jack", 34)
writeToFile(filename, "Jack", 5)
writeToFile(filename, "Jack", 12)
#print(SortAndCompareScores(filename, 77))
#readFromFileAndPrint(filename)
'''
#displayScores(filename, 5)


    






    

