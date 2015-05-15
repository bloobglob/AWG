# Author: Daniel Commins 
# Date:   May 14, 2015
# Files:  AWG_py3.py; SINGLE.TXT (dictionary words file)
# Tested: python 2.61 (converted to python 3 compatibility using 2to3 lib)
# Info:   Akemi's Word Game: The game where you try and guess the computer's randomly
#         selected word!

import sys
import random

# Global vars
gMinLetters = 4
gMaxLetters = 12
gMaxAttempts = 10
gGameTitle = "Akemi's Word Game"

debug = 0       # non-zero to print out debug info

gListOfReadWords = list()
gWordList = list()
#gWordList = [ 'blahh', 'hello', 'world', 'foool', 'barrr' ]

# Determines if passed in string is an integer
def Is_Str_Integer( str ) :
    try :
        int( str )
        return True
    except:
        return False

# Get string from user
def GetInput( str ) :
    if ( sys.version[0] < '3' ) :
        retStr = input( str )
    else :
        retStr = eval(input( str ))
        
    return ( retStr )

# Pick valid number of words in secret word
def PickNumLetters() :
    while ( True ) :

        numLettersStr = GetInput( "Enter the number of letters in secret word [%d-%d]: " %(gMinLetters, gMaxLetters) )
            
        if ( ( Is_Str_Integer( numLettersStr ) is False ) )  :
            print("ERROR: Invalid number of letters")
            continue
        else :
            numLetters = int( numLettersStr )
            if ( ( numLetters < gMinLetters ) or ( numLetters > gMaxLetters ) ) :
                print("ERROR: enter a number between", gMinLetters, "and", gMaxLetters)
            else :
                # Valid number of letters chosen
                break
    return ( numLetters )

def PickNumAttempts() :
    while ( True ) :

        numAttemptsStr = GetInput( "Enter the number of guesses [1-%d]: " %(gMaxAttempts) )

        if ( ( Is_Str_Integer( numAttemptsStr ) is False ) )  :
            print("ERROR: Invalid number of attempts")
            continue
        else :
            numAttempts = int( numAttemptsStr )
            if ( ( numAttempts < 1 ) or ( numAttempts > gMaxAttempts ) ) :
                print("ERROR: enter a number between 1 and", gMaxAttempts)
            else :
                # Valid number of letters chosen
                break
    return ( numAttempts )

def GetRandomWord( listOfWords, numLetters ) :
    randomWord = None

    # TODO: optimize so that the list doesn't have to be re-created
    # if the same number of letters are chosen
    del gWordList[:]

    # Make sure to omit pronouns and words that are the incorrect length
    for word in listOfWords :
        if ( len(word) == numLetters ) :
            if ( ( word[0] >= 'a' ) and ( word[0] <= 'z' ) ) :
                gWordList.append(word)
    
    # Make sure the list is populated with words
    if ( len(gWordList) != 0 ) :
        # Reselect if the same word comes up twice?????
        randomIndex = random.randint( 0, ( len( gWordList ) - 1 ) )
        randomWord = gWordList[ randomIndex ]

    return ( randomWord )

def GetGuessWord( chance, numLetters ) :
    while ( True ) :
        guessWord = GetInput( "Guess %d: " %(chance) )
    
        # Check for correct num letters
        if ( len( guessWord ) != numLetters ) :
            print("Guess word does not contain %d letters, guess again" %(numLetters))
        else :
            invalidLetter = False
            
            for letter in guessWord :
                if ( ( letter < 'a' ) or ( letter > 'z' ) ) :
                    invalidLetter = True
                    break
            
            if ( invalidLetter == True ) :
                print("Guess word does not contain all letters, guess again")
            else :
                # Valid guess
                break    
            
    return ( guessWord.lower() )

def OpenWordsFile() :
    fileHandle = None
    wordFile = "SINGLE.TXT"

    try:
        fileHandle = open( wordFile )
    except:
        print('ERROR: Unable to open word file: ' + wordFile)

    return ( fileHandle )

if __name__ == '__main__':
    wordListHandle = None
    changeParams = True            # User has to pick params first time
    chances = 5

    # Open and read large words file once
    wordListHandle = OpenWordsFile()
    if ( wordListHandle == None ) :
        print("Unable to open file containing the list of words")
        quit()
        
    gListOfReadWords = wordListHandle.read().splitlines()

    print("\n-----------------------------------------------------------------------------")
    print("Welcome to "+gGameTitle+"!")
    print("Guess at the randomly chosen n-letter word")
    print("X = correct letter, wrong location")
    print("O = correct letter and location")
    print("_ = letter not used in word")
    # What if a letter is used more than once? Are plurals legal?

    # Main game loop; stay inside until player wants to exit
    while ( True ) :
        resultList = list()

        if ( changeParams != 0 ) :
            # User picks the number of characters in secret word
            numLetters = PickNumLetters()
    
            # User picks the number of attempts at the secret word
            chances = PickNumAttempts()
    
        # Computer picks a random word containing the selected characters
        randomWord = GetRandomWord( gListOfReadWords, numLetters )

        if ( debug != 0 ) :
            print("Random word = ", randomWord)
            print("Chances = ", chances)
            print("Number of letters = ", numLetters)
            #quit()

        # Display the screen for the game; a line for each number of attempts
        while ( chances > 0 ) :
            wrongLetters = 0

            # User guesses the word
            guess = GetGuessWord( chances, numLetters )
        
            del resultList[:]
        
            # Game gives clues as to which letters are correct and in the right location
            for index, letter in enumerate( guess ) :
                if ( letter in randomWord ) :
                    if ( guess[index] == randomWord[index] ) :
                        resultList.append("O")
                    else :
                        resultList.append("X")
                        wrongLetters = wrongLetters + 1
                else :
                    resultList.append("_")
                    wrongLetters = wrongLetters + 1

            if ( wrongLetters == 0 ) :
                print("Correct!")
                break
            else :
                #     "Guess %d:"
                print("         " + ''.join(resultList))     # char list to string
        
            chances = chances - 1
   
        if ( chances == 0 ) :
            print("The word was:", randomWord)
   
        # Replay????
        replay = GetInput( "Play again? [y=yes; n=no; m=change letters/guesses]" )

        if replay == 'y' :
            changeParams = False
        elif replay == 'm' :
            changeParams = True
        else :
            # Exit game
            break
