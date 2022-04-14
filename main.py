import random 
#from os import *
import sys 
import os
from collections import *
import math


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

ranking = defaultdict(lambda: 0)

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
def unigramTokens (authorsParam):   
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
    testWordCount = 0 
    geoMean = 0
    #exp(1/n* sum(log(p(word)))
    
    #ranking = defaultdict(lambda: 0)

    #ranking['testfile'] = defaultdict(lambda: 0)
    for filename in os.listdir('test'): #for every file in test directory 
        f = os.path.join('test',filename)   #get the path 
        file = open(f,'r').readlines()  #read each file 
        testAuthor = filename[:-4] #get the test author name from the file 
        ranking[testAuthor] = defaultdict(lambda: 0) #create a dictionary 
        testWordCount = 0 #wordcount 
        for author in unigramModels:  #for every author in unigramModels 
            sumNum = 0 
            for line in file: 
                words = line.split()
                words = words[4:] 
                #authorTestTokens['testfile'] += len(words)
                for word in words: 
                    #1. we need to get the number of tokens per test file
                    testWordCount += 1 
                    #print("Trained Probability: " + str(word) + str(unigramModels['trainfile'][word]))
                    sumNum += math.log(unigramModels[author][word], 2)
                    #print(sumNum)
            #find the trained probability of the test-word 
            geoMean = math.pow(2,(1/testWordCount)*sumNum)
            #2. we need to store the sums per author per testfile 
            ranking[testAuthor][author] = geoMean 

    print(ranking['8239592']) 


# Task 4 : Singleton: 



#Main

#randomFiles() 
unigramTokens(authorTokens)
#print(unigramModels['testfile']) 
AllTokens()
