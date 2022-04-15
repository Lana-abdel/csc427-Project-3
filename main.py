import random 
#from os import *
import sys 
import os
from collections import *
import math 
from operator import getitem
from operator import itemgetter

#size of vocabulary
vocabSize = 0
#size of vocabulary for each author
authorTokens = defaultdict(lambda: 0)
#size of vocabulary for each testfile  author
authorTestTokens = defaultdict(lambda: 0)
#62 Unigram Models
unigramModels = defaultdict(lambda: 0)
#Unigram model of all words
vocab = defaultdict(lambda: 0)

# Task 2 - Create train and test files
def randomFiles():
    count = 0
    sampleInput = open(sys.argv[1], 'r').readlines()
    randomTestNum = []
    randomTrainNum = []
            
    while len(randomTestNum) < 100 or len(randomTrainNum) < 900:
        rand = random.randint(1,1000)
        if (rand not in randomTestNum and len(randomTestNum) < 100):
            randomTestNum.append(rand)
        elif (rand not in randomTrainNum and len(randomTrainNum) < 900):
            randomTrainNum.append(rand)
       
    # a for loop to populate both test and train in one go
    for i in range(0,62):
        startingLine = i * 1000
        tabSeparated = sampleInput[startingLine].split(" ")[0]
        author = tabSeparated.split("\t")[1] #authorname for filename
        test = open(sys.argv[3]+"/"+author+'.txt', 'w')
        train = open(sys.argv[2]+"/"+author+'.txt', 'w')
        for line in range(startingLine, startingLine+1000):
            #print(line)
            if (line%1000) in randomTestNum:
                #add to test folder, authorID.txt
                test.write(sampleInput[line])
            else:
                train.write(sampleInput[line])
    

#Task 3 - Unigram Probabilities
def unigramTokens():   
    sampleInput = open(sys.argv[1], 'r').readlines()
    
    for line in sampleInput: 
        words= line.split()
        words = words[4:]
        for word in words: 
            #print(word)
            vocab[word] += 1
            
    
    for filename in os.listdir('train'):
        f = os.path.join('train', filename)
    # checking if it is a file
        if os.path.isfile(f):
            #print(filename)
            file = open(f,'r').readlines()
            author = filename[:-4]
            #adding new author
            unigramModels[author] = defaultdict(lambda: 0)
            
            for line in file:
                words = line.split()
                words = words[4:]
                authorTokens[author] += len(words)
                for word in words:
                    #vocab[word] += 1
                    unigramModels[author][word] += 1
                    
                        

    # an unknown word appears in that author's test set but not its train set
    # consider each author's vocab separately
    
    vocabSize = len(vocab) #vocabulary size
    #print("VocabSize: " + str(vocabSize))
    for author in unigramModels: 
        for item in vocab:
            if (item in unigramModels[author]):
                unigramModels[author][item] = (unigramModels[author][item]+1)/ (authorTokens[author] + vocabSize)
            else: 
                unigramModels[author][item] = 1 / (authorTokens[author] + vocabSize)


#Task 4: AllTokens: 
def AllTokens(): 
    sumNum=0
    #testWordCount = 0 
    geoMean = 0
    ranking = defaultdict(lambda: 0)
    
    #ranking = defaultdict(lambda: 0)

    #ranking['testfile'] = defaultdict(lambda: 0)
    for filename in os.listdir('test'): #for every file in test directory 
        f = os.path.join('test',filename)   #get the path 
        file = open(f,'r').readlines()  #read each file 
        testAuthor = filename[:-4] #get the test author name from the file 
        ranking[testAuthor] = defaultdict(lambda: 0) #create a dictionary 
        for author in unigramModels:  #for every author in unigramModels 
            sumNum = 0
            testWordCount = 0 #wordcount 
            #for every review by the current test author
            for line in file: 
                words = line.split()
                #get 1 line -> 1 review
                words = words[4:]
                testWordCount += len(words)
                #authorTestTokens['testfile'] += len(words)
                for word in words: 
                    #1. we need to get the number of tokens per test file
                    #testWordCount += 1 
                    #if testAuthor == 'testfile':
                        #print("The sumNum for tf is: "+str(sumNum))
                        #print("testWordCount is: "+str(testWordCount))
                        #print("The geoMean is: "+str(geoMean))
                    #print("Trained Probability: " + str(word) + str(unigramModels['trainfile'][word]))
                    sumNum += math.log(unigramModels[author][word], 2)
                    #print(sumNum)
                
            #find the trained probability of the test-word 
            # if(testAuthor == 'testfile'):
            #     print(testWordCount)
            geoMean = math.pow(2,(1/testWordCount)*sumNum)
            
            #2. we need to store the sums per author per testfile 
            
            #testAuthor is every author from the test dir. Author is every author from the train, unigramModel
            ranking[testAuthor][author] = geoMean 

    scores = [(outer_key,inner_key,value) for outer_key, inner in ranking.items() for inner_key, value in inner.items() if outer_key.endswith('33913')]
    scores.sort(key=lambda x: (-x[2], len(x[1])))
    print(scores)

    #sorted(score, key=lambda x,y: (ranking[x][y]))
    #print("33913 : " + str(ranking['33913']))
    #print("70535 : " + str(ranking['70535']))
    #print(score)

# Task 4 : Singleton: 

def Singleton(): 
    geoMean = 0
    ranking = defaultdict(lambda: 0) # to create a nested dictionary for all geometric means

    #for filename in os.listdir('test'): 
    f = os.path.join('test','testfile.txt')
    file = open(f,'r').readlines()  #read each file 
    #testAuthor = filename[:-4] #get the test author name from the file 
    ranking['testfile'] = defaultdict(lambda: 0) #create a dictionary 
    for author in unigramModels:
        onecounts = defaultdict(lambda: 0)
        sumNum = 0
        for line in file:
                words = line.split()
                words = words[4:]
                for word in words:
                    
                    onecounts[word] += 1
                    
        for item in onecounts:
            #print(item)
            if onecounts[item] == 1: 
                #print(item)
                #print("author: " + str(author))
                #print("Trained Probability: " + str(item) + " " + str(unigramModels[author][item]))
                sumNum += math.log(unigramModels[author][item], 2)  
        
        #print("sumNum: "+ str(sumNum))
        #print("total length of one counts : " + str(len(onecounts)))
        geoMean = math.pow(2,(1/len(onecounts))*sumNum)
        #print(geoMean)
            #2. we need to store the sums per author per testfile 
        ranking['testfile'][author] = geoMean 
    
    # def sortRankingDict(dict):
    #     score = []
    #     sorted(score, key=lambda x: (dict[x][author]))
    
    
    
   #stuff we tried to sort a dictionary.  
    #print(ranking)
    #print(len(ranking))
    #res = ranking.sort(key=lambda e: e['testfile'][author], reverse=True)
    #res = dict(sorted(ranking, key=lambda x: (ranking[1][author]), reverse = True))
    #print(res)
    #print(itemgetter(ranking['testfile'][author])) 






#randomFiles()
unigramTokens()
#print(unigramModels['testfile']) 
AllTokens()

#Singleton()
