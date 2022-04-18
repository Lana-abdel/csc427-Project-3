# csc427-Project-3
## Authors: Lana Abdelmohsen, Robert Helck, Casey Lishko, Alex Quezada
## Description 
This package implements two authorship attribution systems, AllTokens and Singleton, which calculate the most likely authors of test files from a set of training files.
### What you will find  
- main.py: Our main source code for T2,T3,T4,T5
    - code description: 
      -  randomFiles(): Satisfies the requirements of T1 by producing the train and test directories. 
      -  The unigramTokens(): Function carries out T3 to calculate the Add-1 unigram probabilities.
      -  AllTokens(): For the test file under consideration, it will compute the geometric mean of the unigram probabilities for a candidate author for all the tokens in the test file. Higher scores indicate stronger system belief in authorship. Satisfies T4.
      -  Singleton(): Compute the geometric mean of the unigram probabilities for a candidate author for only the distinct tokens that occur exactly one and only one single time in the test file. Satisfies T4.
      -  rankList(): Ranks each author in the train set by likelihood that they wrote the passed test file, a placement from 1 to 62.  
      -  main(): Function prompts the user for the system whose output they would like to see, AllTokens or Singleton, then calls its associated functions.
 
- Two sub-folders: 
  -  Train directory: All the randomly generated train files per author 
  -  Test Directory: All the randomly generated test files per author  
 
- imdb62.txt: 62,000-line file for all authors and their reviews

- D3.pdf: The written report of our authorship attribution system comparisons (satisfies T5) 
        
- D4.pdf: Contains our reflections about this project



### Instructions for command line 

Prior to running the program, ensure that you have the correct version of python by typing the command

    python --version

into the terminal. If it is not 3.8.6, then enter

    module add python/3.8.6

To run the program, type

    python main.py imdb62.txt ./train ./test

- The user will see the prompt "AllTokens or Singleton? " and enter which of the two authorship attribution systems they would like to observe. 
    -  If they type AllTokens, the program will take a few minutes to run and output two lists: one, the system's rankings for each author's likelihood of writing the test file "33913.txt," and two, for the test file "70535.txt," based on geometric means over all tokens in the test file. Typing Singleton at the prompt will output the other system's determinations for these test files, only considering distinct tokens in the geometric mean calculations. Every list is labeled accordingly with the system that produced it and the test file it attributed.
