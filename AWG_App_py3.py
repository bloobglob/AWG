# Author: Daniel Commins 
# Date:   May 14, 2015
# Files:  AWG_App_py3.py; SINGLE.TXT (dictionary words file)
# Tested: python 2.61 (converted to python 3 compatibility using 2to3 lib)
# Info:   Akemi's Word Game: The game where you try and guess the computer's randomly
#         selected word!

import sys
import random
import tkinter

class CurGuess_t :
    def __init__(self) :
        self.entry = None
        self.button = None

class PastGuesses_t :
    def __init__(self) :
        self.pastGuess = None
        self.result = None
        self.guess = None
        self.matches = None

class WordGame_tk( tkinter.Tk ) :
    entryWidth = 30         # in chars
    guessStartRow = 5       # using grid()
    dictWordList = None     # only needs to be read once for all instances

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.minLetters = 4
        self.maxLetters = 12
        self.maxAttempts = 10
        self.numLetters = None                  # number of letters in word once game starts
        self.numGuesses = None                  # number of guesses at word once game starts
        self.curGuessNum = None                 # tracks users guesses so far
        self.curGuess = CurGuess_t()            # contains widget for the user entry widgets
        self.guesses = [PastGuesses_t() for i in range( self.maxAttempts )]        # one for each guess that can be made
        self.statusText = tkinter.StringVar()   # string message on the status line
        self.statusLabel = None                 # status label widget
        self.randomWord = None                  # randomly selected word from dictionary
        self.wordList = list()                  # stores words from dictionary of the specified length

        # Open and read large words file once if necessary
        self.ReadWordsFile()

        # Set grid geometry
        self.grid()

        lettersText = tkinter.Label( self, anchor="w", text="Number of Letters [%d-%d]" %(self.minLetters, self.maxLetters) )
        lettersText.grid( row=0, column=0, sticky='w' )

        self.lettersEntry = tkinter.Spinbox( self, from_=self.minLetters, to=self.maxLetters, width=3 )
        self.lettersEntry.grid( row=0, column=1, sticky='w' )
        self.lettersEntry.delete( 0, 3 )
        self.lettersEntry.insert( 0, '5' )

        numGuessesText = tkinter.Label( self, anchor="w", text="Number of Guesses [1-%d]" %(self.maxAttempts) )
        numGuessesText.grid( row=1, column=0, sticky='w' )

        self.guessesEntry = tkinter.Spinbox( self, from_="1", to=self.maxAttempts, width=3 )
        self.guessesEntry.grid( row=1, column=1, sticky='w' )
        self.guessesEntry.delete( 0, 3 )
        self.guessesEntry.insert( 0, '5' )

        legendText1 = tkinter.Label( self, anchor='w', text="X = right letter, wrong location", borderwidth=0, bg='cyan', padx=4, width=WordGame_tk.entryWidth )
        legendText2 = tkinter.Label( self, anchor='w', text="O = right letter, right location", borderwidth=0, bg='green', padx=4, width=WordGame_tk.entryWidth )
        legendText3 = tkinter.Label( self, anchor='w', text="_ = letter not in word", borderwidth=0, bg='red', padx=4, width=WordGame_tk.entryWidth )
        legendText1.grid( row=2, column=0, sticky='w')
        legendText2.grid( row=3, column=0, sticky='w')
        legendText3.grid( row=4, column=0, sticky='w')

        quitButton = tkinter.Button( self, text="Exit", borderwidth=0, justify='center', width=len('Start'), command=self.OnExit )
        quitButton.grid( row=2, column=1, sticky='n', rowspan=2 )

        startButton = tkinter.Button( self, text="Start", borderwidth=0, justify='center', width=len('Start'), command=self.OnStart )
        startButton.grid( row=3, column=1, sticky='s', rowspan=2 )

    def OnExit(self) :
        self.destroy()       # So dramatic!

    def OnStart(self) :
        # Get number of guesses and letters here only ONCE when the game starts
        try :
            self.numLetters = int( self.lettersEntry.get() )
        except :
            self.numLetters = None
        try :
            self.numGuesses = int( self.guessesEntry.get() )
        except :
            self.numGuesses = None

        # Check for valid input parameters and get random word
        if ( self.numGuesses == None or self.numGuesses > self.maxAttempts or self.numGuesses <= 0 or
             self.numLetters == None or self.numLetters > self.maxLetters or self.numLetters < self.minLetters ) :
            statusText = "Invalid input parameters!"
            self.numLetters = None
            self.numGuesses = None
        else :
            statusText = "Guess the '%d' letter word!" %(self.numLetters)
            self.randomWord = self.GetRandomWord( WordGame_tk.dictWordList, self.numLetters )

        # Reset the number of guesses
        self.curGuessNum = 0
        
        startRow = WordGame_tk.guessStartRow

        # Print status label if necessary
        if self.statusLabel == None :
            self.statusLabel = tkinter.Label( self, textvariable=self.statusText, borderwidth=0, width=WordGame_tk.entryWidth )
            self.statusLabel.grid( row=startRow, column=0 )
        else :
            self.statusLabel.grid()
        self.statusText.set( statusText )

        startRow = ( startRow + 1 )

        # Print user guess entry field if necessary
        if self.numLetters != None :
            if self.curGuess.entry == None :
                self.curGuess.entry = tkinter.Entry( self, borderwidth=0, width=WordGame_tk.entryWidth, bg='gray80', state='normal' )
                self.curGuess.entry.insert( 0, "<Enter Guess>" )
                self.curGuess.entry.grid( row=startRow, column=0 )
            else :
                self.curGuess.entry.grid()
                self.curGuess.entry.delete( 0, 'end' )
            
        # Print the user guess button if necessary
        if self.numLetters != None :
            if self.curGuess.button == None :
                self.curGuess.button = tkinter.Button( self, text="Guess", borderwidth=0, justify='center', width=len('Start'), command=self.OnGuess )        
                self.curGuess.button.grid( row=startRow-1, column=1, sticky='s', rowspan=2 ) # -1 because rowspan=2
            else :
                self.curGuess.button.grid()
            
        startRow = ( startRow + 1 )

        # First time 'Start' is pressed, create all the guess entries and leave them blank
        # TODO: Possibly reverse the if and for statements
        if self.guesses[0].pastGuess == None :
            for eachGuess in range( self.maxAttempts ) :
                self.guesses[eachGuess].guess = tkinter.StringVar()
                self.guesses[eachGuess].matches = tkinter.StringVar()
                self.guesses[eachGuess].guess.set( "" )
                self.guesses[eachGuess].matches.set( "" )
                
                self.guesses[eachGuess].pastGuess = tkinter.Label( self, textvariable=self.guesses[eachGuess].guess, borderwidth=0, anchor='w', width=WordGame_tk.entryWidth )
                self.guesses[eachGuess].result = tkinter.Label( self, textvariable=self.guesses[eachGuess].matches, borderwidth=0, anchor='w', width=WordGame_tk.entryWidth )
                
                self.guesses[eachGuess].pastGuess.grid( row=startRow, column=0 )
                self.guesses[eachGuess].result.grid( row=(startRow+1), column=0 )
            
                startRow = ( startRow + 2 )

        # Show and hide the guess entries based on how many guesses the user selected
        for eachGuess in range( self.maxAttempts ) :
            # Clear all previous guess and result data output
            self.guesses[eachGuess].guess.set( "" )
            self.guesses[eachGuess].matches.set( "" )
        
            if eachGuess < self.numGuesses :
                # Show the guess entry
                self.guesses[eachGuess].pastGuess.grid()
                self.guesses[eachGuess].result.grid()
            else :
                # Hide the guess entry
                self.guesses[eachGuess].pastGuess.grid_remove()
                self.guesses[eachGuess].result.grid_remove()

    def OnGuess(self) :
        # Check users guess string
        userGuess = self.curGuess.entry.get().lower()

        # Check for valid word length
        if len(userGuess) != self.numLetters :
            self.statusText.set( "Error: Please input '%d' letters" %(self.numLetters) )
        else :
            # Check for valid symbols in word
            invalidLetter = False
            for letter in userGuess :
                if ( ( letter < 'a' ) or ( letter > 'z' ) ) :
                    invalidLetter = True
                    break
            
            if ( invalidLetter == True ) :
                self.statusText.set( "Error: Invalid symbols in word" )  
            else :
                # Valid entry! Check letter matches with the random word
                resultList = list()
                wrongLetters = 0
                
                # Loop letters in guess word, checking letter in word, then correct position
                for index, letter in enumerate( userGuess ) :
                    if letter in self.randomWord :
                        if ( userGuess[index] == self.randomWord[index] ) :
                            resultList.append("O")
                        else :
                            resultList.append("X")
                            wrongLetters = wrongLetters + 1
                    else :
                        resultList.append("_")
                        wrongLetters = wrongLetters + 1

                if wrongLetters == 0 :
                    # Correct guess!
                    self.OnMatch()
                else :
                    # Incorrect guess! Print the resulting letter matches.
                    # String join method to convert list of chars to string
                    guessNumStr = "%2d: " %(self.curGuessNum+1)
                                                              # "00: "
                    self.guesses[self.curGuessNum].matches.set( "    "+"".join(resultList) )
                    self.guesses[self.curGuessNum].guess.set( guessNumStr+userGuess )
                    
                    self.curGuessNum = ( self.curGuessNum + 1 )
                    
                    if self.curGuessNum < int( self.numGuesses ) :
                        # Still more chances to guess...
                        self.statusText.set( "<Guess %d/%d>" %((self.curGuessNum+1), self.numGuesses ) )
                        self.curGuess.entry.delete( 0, 'end' )
                    else :
                        # No more chances, game over :(
                        self.statusText.set( "Random word was: "+self.randomWord )
                        self.curGuess.button.grid_remove()
        
    def GetRandomWord( self, listOfWords, numLetters ) :
        randomWord = None

        # TODO: optimize so that the list doesn't have to be re-created
        # if the same number of letters are chosen
        del self.wordList[:]

        # Make sure to omit pronouns and words that are the incorrect length
        for word in WordGame_tk.dictWordList :
            if ( len(word) == numLetters ) :
                if ( ( word[0] >= 'a' ) and ( word[0] <= 'z' ) ) :
                    self.wordList.append(word)
    
        # Make sure the list is populated with words
        if ( len(self.wordList) != 0 ) :
            randomIndex = random.randint( 0, ( len( self.wordList ) - 1 ) )
            randomWord = self.wordList[ randomIndex ]    

        return ( randomWord )

    def OnMatch(self) :
        self.statusText.set( "Correct guess, YOU WIN!!!"  )
        self.curGuess.button.grid_remove()

    def ReadWordsFile(self) :
        # Only need to be read once
        if ( WordGame_tk.dictWordList == None ) :
            fileHandle = None
            wordFile = "SINGLE.TXT"

            try:
                fileHandle = open( wordFile )
            except:
                print('ERROR: Unable to open word file: ' + wordFile)

            # Can't proceed unless the program can get a random word
            if ( fileHandle == None ) :
                self.destroy()
        
            # Populate list with all words read from file
            WordGame_tk.dictWordList = fileHandle.read().splitlines()


if __name__ == '__main__':
    game = WordGame_tk(None)
    game.title("AKEMI's Word Game")
    game.mainloop()
    