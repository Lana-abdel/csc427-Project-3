# Names: Lana Abdelmohsen, Robert Helck, Casey Lishko, Alex Quezada
# Project Title: Authorship Attribution
# File: main.py
# Description: This program attributes test files to authors of train files in two ways, first by
# considering all tokens in the test file and then only distinct tokens.

import random 
import sys 
import os
from collections import *
import math

# This variable holds the size of vocabulary.
vocabSize = 0
# This defaultdict holds the number of tokens for each author.
authorTokens = defaultdict(lambda: 0)
# This is a defaultdict with a key for each author, and a value for the number of tokens associated with each author.
authorTestTokens = defaultdict(lambda: 0)
# This is a defaultdict for the 62 Unigram Models, with the models as values and authors as keys.
unigramModels = defaultdict(lambda: 0)
# This is a default dicts with a key for each word in a vocabulary, and values of the counts thereof.
vocab = defaultdict(lambda: 0)

# Task 2 - Create train and test files
def randomFiles():
    '''
     RandomFiles() does not take any arguments. It reads from imdb62.txt
     and assigns 90 percent of its lines to training files, and the 
     other 10 percent of test files. '''

    # The variabels sampleInput contains data from imdb62.txt.
    sampleInput = open(sys.argv[1], 'r').readlines()
    # The list randomTestNum contains line numbers from imdb62.txt , which are used to create the test set.
    randomTestNum = []
    
    # This while loop populates randomTestNum with random numbers which correspond to lines in imdb62.txt.
    while len(randomTestNum) < 100:
        rand = random.randint(1,1000)
        if (rand not in randomTestNum and len(randomTestNum) < 100):
            randomTestNum.append(rand)
       
    # For loop to populate both test and train directories with .txt files corresponding to reviews of each author.
    for i in range(0,62):
        #Variable startingLine stores the "i-thousandth" line, i.e. the first review for author i.
        startingLine = i * 1000
        tabSeparated = sampleInput[startingLine].split(" ")[0]
        # This line finds the author name for the file.
        author = tabSeparated.split("\t")[1] 
        test = open(sys.argv[3]+"/"+author+'.txt', 'w')
        train = open(sys.argv[2]+"/"+author+'.txt', 'w')
        # For all reviews for an author...
        for line in range(startingLine, startingLine+1000):
            if (line%1000) in randomTestNum:
                # ...add each review to the test folder for the current author.
                test.write(sampleInput[line])
            else:
                # add each review to the train folder for the current author.
                train.write(sampleInput[line])

# Task 3 - Unigram Probabilities
def unigramTokens():   
    '''
     UnigramTokens() takes no parameters. It reads files in the train subdirectory
     and calculates unigram probabilities for each author in the training sets. '''
    
    sampleInput = open(sys.argv[1], 'r').readlines()
    
    # Finds the word count for all words in imdb62.txt.
    for line in sampleInput: 
        words= line.split()
        words = words[4:]
        for word in words: 
            vocab[word] += 1
            
    # Create separate unigrams for all words in each author inside the train directory
    for filename in os.listdir('train'):
        f = os.path.join('train', filename)
        # Checking to see if train/filename is an existing file
        if os.path.isfile(f):
            file = open(f,'r').readlines()
            # the author is the name of the file without .txt
            author = filename[:-4]
            # add each author to unigramModels
            unigramModels[author] = defaultdict(lambda: 0)
            
            ## For each review (a.k.a. line), we add the cardinality of the tokens in that review 
            ## to tokens, and add the count of the individual words to unigramModels on a per author basis.
            for line in file:
                words = line.split()
                words = words[4:]
                authorTokens[author] += len(words)
                for word in words:
                    unigramModels[author][word] += 1
    
    # Variable vocabSize hold the number of unique tokens.
    vocabSize = len(vocab)
    '''
     For each author-word combination, assign a probability model in unigramModels[][].
     Each item represents a distinct word, and never a duplicate token, since it is taking the 
     keys of the vocab dictionary (a hash table). '''
    for author in unigramModels: 
        for item in vocab:
            if (item in unigramModels[author]):
                unigramModels[author][item] = (unigramModels[author][item]+1)/ (authorTokens[author] + vocabSize)
            else: 
                ## This handles cases of a word appearing in the vocabulary but not in the current training author's vocabulary.
                unigramModels[author][item] = 1 / (authorTokens[author] + vocabSize)


# Task 4 - AllTokens
def AllTokens(): 
    '''
     AllTokens takes no parameters. This is an author attribution system that calculates
     the geometric mean of the unigram probabilities for an author using all the
     tokens in the author test file. '''
    
    # Sum of the logs of the unigram probabilities.
    sumNum=0
    # Geometric mean of all unigram probabilities.
    geoMean = 0
    # Dictionary to record authorship attribution scores.
    attributeScores= defaultdict(lambda: 0)
    # For every file in test directory... 
    for filename in os.listdir('test'):
        # Save the path to f...  
        f = os.path.join('test',filename)   
        # ... and read the file and save it to file variable.
        file = open(f,'r').readlines()
        # Get the test author name from the file.
        testAuthor = filename[:-4]  
        # create a new dictionary key with the current test author
        attributeScores[testAuthor] = defaultdict(lambda: 0) 
        # for every author in unigramModels, calculate the author attribution score
        # for the current test file with all the train files
        for author in unigramModels:  
            sumNum = 0
            # word count of test file
            testWordCount = 0
            # for every word in the test file, calculate log2(P(word)) and keep a running sum
            for line in file: 
                words = line.split()
                words = words[4:]
                testWordCount += len(words)
                for word in words: 
                    sumNum += math.log(unigramModels[author][word], 2)
                
            # find the trained probability of the test-word 
            geoMean = math.pow(2,(1/testWordCount)*sumNum)

            # record authorship attribution score of the test author when compared to the current author
            attributeScores[testAuthor][author] = geoMean
    
    # output of authorship attribution scores
    print("AllTokens 33913: ")
    rankList(attributeScores,'33913')
    print("AllTokens 70535: ")
    rankList(attributeScores,'70535')

# Task 4 - Singleton
def Singleton():  
    '''
     Singleton takes no parameters. This is an author attribution system that calculates
     the geometric mean of the unigram probabilities for an author using all the
     UNIQUE tokens in the author test file. '''

    # to create a nested dictionary for all geometric means
    attributeScores = defaultdict(lambda: 0) 

    for filename in os.listdir('test'): 
        f = os.path.join('test',filename)
        # read each file 
        file = open(f,'r').readlines()
        # get the author name from the test file
        testAuthor = filename[:-4]

        ## nest the dictionary we created prior to this loop so that each test file author can be paired with an author of a train file
        ## and the geometric mean (authorship attribution score) can be stored as the value
        attributeScores[testAuthor] = defaultdict(lambda: 0)

        # for every author in the train set
        for author in unigramModels:

            # create a dictionary to store the count of all words that will appear in a file
            nondistinctTokens = defaultdict(lambda: 0)
            # reset the variable that contains the running total of unigram probabilities
            sumNum = 0
            for line in file:
                words = line.split()
                # redeclare the array so that the numerical information that starts each line is omitted
                words = words[4:]
                for word in words:
                    # add occurrences of word to an index in nondistinctTokens
                    nondistinctTokens[word] += 1
            
            # the length of nondistinctTokens (number of indices) will be the number of distinct tokens in the file
            uniqueTokens = len(nondistinctTokens)

            # start calculating the geometric mean only for distinct tokens which are those that occur once in nondistinctTokens
            for item in nondistinctTokens:
                if nondistinctTokens[item] == 1:
                    sumNum += math.log(unigramModels[author][item], 2)  

            ## calculate and store the geometric mean for the test file and train file author combination
            ## but catch the division-by-zero error when a test file has no distinct tokens (all duplicate lines)
            try:
                geoMean = math.pow(2,(1/uniqueTokens)*sumNum)
                attributeScores[testAuthor][author] = geoMean
            except ZeroDivisionError:
                print("File " + str(file) + " contains no unique tokens!")
                sys.exit(1)

    # output of authorship attribution scores
    print("Singleton 33913: ")
    rankList(attributeScores,'33913')
    print("Singleton 70535: ")
    rankList(attributeScores,'70535')

# Task 5 - Rank the authors from most to least likely (1-62) to have written the passed file
def rankList(nestedDict,fileNumber): 
    '''
     rankList takes two arguments, a nested dictionary with an author of a test file as the outer key
     and the author of a train file as the inner key, and the name of the test file without the extension
     It outputs a sorted list of 2-tuples, which correspond to an author in the train set and their
     ranking from 1 to 62 of how likely they were to have written the parameter file (highest to lowest geometric mean)'''
    
    # this will store the sorted tuples
    rankinglist = []
    
    # produces a 3-tuple of the test file author, train file author, and geometric mean, for the passed test file
    geoMeanTuples = [(outer_key,inner_key,value) for outer_key, inner in nestedDict.items() for inner_key,value in inner.items() if outer_key.endswith(fileNumber)]
    
    # sort the tuples in descending order by their geometric means
    geoMeanTuples.sort(key=lambda x: (-x[2], len(x[1])))

    # start the ranking at 1
    rank=1

    ## for every 3-tuple in geoMeanTuples, append the author of a train file b followed by their rank
    ## to the list as a 2-tuple
    for a,b,c in geoMeanTuples:
        rankinglist.append(tuple((b,rank)))

        # move onto the next tuple in geoMeanTuples, which will get the next rank
        rank += 1
    
    # print the list
    print(rankinglist)

# main function
def main(): 
    '''
     The main function takes no parameters, but it decides which authorship attribution system to call
     depending on whether the user enters AllTokens or Singleton at the command line '''

    system = input("AllTokens or Singleton? ")
    if system == "AllTokens":
        randomFiles()
        unigramTokens()
        AllTokens()
    elif system == "Singleton":
        randomFiles()
        unigramTokens()
        Singleton()
    else:
        print("Enter a valid system (AllTokens or Singleton).")

if __name__ == "__main__":
    main()
