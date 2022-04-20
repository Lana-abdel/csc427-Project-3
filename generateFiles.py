# Names: Lana Abdelmohsen, Robert Helck, Casey Lishko, Alex Quezada
# Project Title: Authorship Attribution
# File: random.py
# Description: This program splits up imdb62.txt into train and test files. 

import random 
import sys 
from collections import *

# Task 2 - Create train and test files
def randomFiles(file):
    '''
     RandomFiles() takes in the imdb62.txt file as a parameter.  It reads from imdb62.txt
     and assigns 90 percent of its lines to training files, and the 
     other 10 percent of test files. '''

    # The variabels sampleInput contains data from imdb62.txt.
    sampleInput = open(file, 'r').readlines()
    # The list randomTestNum contains line numbers from imdb62.txt , which are used to create the test set.
    randomTestNum = []
    
    # This while loop populates randomTestNum with random numbers which correspond to lines in imdb62.txt.
    while len(randomTestNum) < 100:
        rand = random.randint(1,1000)
        if (rand not in randomTestNum and len(randomTestNum) <= 100):
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
imdb62 = str(sys.argv[1])
randomFiles(imdb62)
print("\n The files have been generated\n")
