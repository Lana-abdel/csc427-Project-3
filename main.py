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
def unigramTokens (authorsParam):   

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
                    vocab[word] += 1
                    unigramModels[author][word] += 1

    vocabSize = len(vocab) #vocabulary size
    for author in unigramModels:
        for word in unigramModels[author]:
            unigramModels[author][word] = (unigramModels[author][word]+1)/ (authorTokens[author] + vocabSize)

def AllTokens(): 
    sumNum=0
    #exp(1/n* sum(log(p(word))) 
    for author in unigramModels: 
            
        #for filename in os.listdir('test'): 
            #f = os.path.join('test',filename)
            f = os.path.join('test','testfile.txt')   
            file = open(f,'r').readlines()
            for line in file: 
                sentence = line.split()
                sentence = sentence[4:]
                print(sentence)
                ###we are ignoring unknowns by doing it like this, also, we do not care about repeats for this method
                for trainedword in unigramModels[author].keys(): 
                    #print("Trainedword1: "+trainedword)
                    if (trainedword in sentence):   
                        print("Trainedword2: "+trainedword)
                        print("Trained Probability: " + str(unigramModels[author][trainedword]))
                        sumNum += math.log(unigramModels[author][trainedword])
                        print(sumNum)
                        print("Author:" + str(author))
                        print(math.exp(sumNum))
                #find the trained probability of the test-word 

        #calculate the number of tokens for a file 

        #calculate the sum of logs of the probabilities for a word in test, if it's unknown ignore it. 
        

        #raise it to the 2^1/n

#Main

#randomFiles() 
unigramTokens(authorTokens)
#print(unigramModels['testfile']) 
AllTokens()
