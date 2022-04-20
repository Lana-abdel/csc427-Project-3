# csc427-Project-3
## Authors: Lana Abdelmohsen, Robert Helck, Casey Lishko, Alex Quezada
## Description 
This package implements two authorship attribution systems, AllTokens and Singleton, which calculate the most likely authors of test files from a set of training files.
### What you will find:  
- main.py: Our source code for T3, T4, and T5
    - Code description: 
      -  The unigramTokens(...): Takes in two parameters the imbd62.txt file and the name of the train file as parameters. It calculates the Add-1 unigram probabilities. Satisfies T3. 
      -  AllTokens(...): Takes the name of the test folder as a parameter. For the test file under consideration, it will compute the geometric mean of the unigram probabilities for a candidate author for all the tokens in the test file. Higher scores indicate stronger system belief in authorship. Satisfies T4.
      -  Singleton(...): Takes the name of the text directory as a parameter. Computes the geometric mean of the unigram probabilities for a candidate author for only the distinct tokens that occur exactly one and only one single time in the test file. Satisfies T4.
      -  rankList(...):  Takes two arguments, a nested dictionary with an author of a test file as the outer key and the author of a train file as the inner key. Ranks each author in the train set by likelihood that they wrote the passed test file, from highest to lowest geometric mean.  
      -  main(): Function prompts the user for the system whose output they would like to see, AllTokens or Singleton, then calls its associated functions.
- generateFiles.py: Our source code for T2
     -   randomFiles(...): Takes in the imdb62.txt file as a parameter. Satisfies the requirements of T2 by producing the randomized files in the train and test directories. 
 
- Two sub-folders: 
  -  Train directory: All the randomly generated train files per author 
  -  Test Directory: All the randomly generated test files per author  
 
- imdb62.txt: 62,000-line file for all authors and their reviews

- D3.pdf: The written report of our authorship attribution system comparisons (satisfies T5) 
        
- D4.pdf: Contains our reflections about this project



### Command line instructions:

Prior to running the program, ensure that you have the correct version of python by typing the command

    python --version

into the terminal. If it is not 3.8.6, then enter

    module add python/3.8.6

To run the program generateFiles.py, type

    python generateFiles.py /path/to/imdb62.txt /path/to/train /path/to/test  
    
output for generateFiles.py: 
    - This will populate the train and test directories specified with 62 files one for each author. 
    - The output displayed would be a confirmation stating that "The files have been generated"
    
To run the main.py program, type

    python main.py /path/to/imdb62.txt /path/to/train /path/to/test  
    
- output for main.py:  
    - The user will see the prompt "AllTokens or Singleton? (type q to quit)" and enter which of the two authorship attribution systems they would like to observe. 
        -  If they type AllTokens, the program will take a few minutes to run and output two lists: 
             - The system's rankings for each author's likelihood of writing the test file "33913.txt," 
             - The system's rankings for each author's likelihood of writing the test file "70535.txt,"
             - The calculation is based on the geometric means over all tokens in the test file. 
             - Typing Singleton at the prompt will output the other system's determinations for these test files, only considering distinct tokens in the geometric mean calculations.
             -  Every list is labeled accordingly with the system that produced it and the test file it attributed.
