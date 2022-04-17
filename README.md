CSC427 Project 3: Authorship Attribution

Our package consists of a test directory, train directory, the file imdb62.txt, and our source code main.py. The written report of our authorship attribution system comparisons can be found in d3.pdf. d4.pdf contains our reflections about this project. In main.py, randomFiles() satisfies the requirements of T1 by producing the train and test directories. The unigramTokens() function carries out T3. AllTokens() and Singleton() implement the respective authorship attribution systems in T4. rankList() ranks each author in the train set by likelihood that they wrote the passed test file, a placement from 1 to 62. The main function prompts the user for the system whose output they would like to see, AllTokens or Singleton, then calls its associated functions.

Prior to running the program, ensure that you have the correct version of python by typing the command

    python --version

into the terminal. If it is not 3.8.6, then enter

    module add python/3.8.6

To run the program, type

    python main.py imdb62.txt ./train ./test

The user will see the prompt "AllTokens or Singleton? " and enter which of the two authorship attribution systems they would like to observe. If they type AllTokens, the program will take
a few minutes to run and output two lists: one, the system's rankings for each author's likelihood of writing the test file "33913.txt," and two, for the test file "70535.txt," based on geometric means over all tokens in the test file. Typing Singleton at the prompt will output the other system's determinations for these test files, only considering distinct tokens in the geometric mean calculations. Every list is labeled accordingly with the system that produced it and the test file it attributed.