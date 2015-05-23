# Title:  AWG - Akemi's Word Game
# Author: Daniel Commins 
# Date:   May 22, 2015
# Files:  AWG_App_py2.py; SINGLE.TXT (dictionary words file)
# Tested: python 2.61
# Info:   Akemi's Word Game: The game where you try and guess the computer's randomly
#         selected word! Each letter appears only once.

import sys
import random
import tkinter
import tkinter.messagebox

GAME_VERSION = "1.2"

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
    guessStartRow = 7       # using grid()
    dictWordList = None     # only needs to be read once for all instances

    def __init__( self, parent ):
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
        self.pluralCheckVal = tkinter.IntVar()  # stores value from user option to include word plurals
        self.checkPlurals = None                # stores the plural check option when game starts

        # Open and read large words file once if necessary
        self.ReadWordsFile()

        # Set grid geometry
        self.grid()

        # Plural checkbox
        pluralCheckButton = tkinter.Checkbutton( self, text="omit 's'/'es' plurals", variable=self.pluralCheckVal, onvalue=1, offvalue=0 )
        pluralCheckButton.grid( row=0, column=0, sticky='w' )
        pluralCheckButton.select()      # enable by default
        
        # Menu button 
        infoButton = tkinter.Button( self, text="Info", borderwidth=0, justify='center', command=self.OnInfo )
        infoButton.grid( row=0, column=1, sticky='n', rowspan=1 )

        # Number of letters option
        lettersText = tkinter.Label( self, anchor='w', text="Number of Letters [%d-%d]" %(self.minLetters, self.maxLetters) )
        lettersText.grid( row=1, column=0, sticky='w' )

        self.lettersEntry = tkinter.Spinbox( self, from_=self.minLetters, to=self.maxLetters, width=3 )
        self.lettersEntry.grid( row=1, column=1, sticky='w' )
        self.lettersEntry.delete( 0, 3 )
        self.lettersEntry.insert( 0, '5' )

        # Number of guesses option
        numGuessesText = tkinter.Label( self, anchor="w", text="Number of Guesses [1-%d]" %(self.maxAttempts) )
        numGuessesText.grid( row=2, column=0, sticky='w' )

        self.guessesEntry = tkinter.Spinbox( self, from_="1", to=self.maxAttempts, width=3 )
        self.guessesEntry.grid( row=2, column=1, sticky='w' )
        self.guessesEntry.delete( 0, 3 )
        self.guessesEntry.insert( 0, '5' )

        # Statement of rules
        legendText1 = tkinter.Label( self, anchor='center', text="*Each letter is used only once*", borderwidth=0, bg='yellow', padx=4, width=WordGame_tk.entryWidth )
        legendText2 = tkinter.Label( self, anchor='w', text="O = right letter, wrong location", borderwidth=0, bg='cyan', padx=4, width=WordGame_tk.entryWidth )
        legendText3 = tkinter.Label( self, anchor='w', text="\u25b2 = right letter, right location", borderwidth=0, bg='green', padx=4, width=WordGame_tk.entryWidth )
        legendText4 = tkinter.Label( self, anchor='w', text="_ = letter not in word", borderwidth=0, bg='red', padx=4, width=WordGame_tk.entryWidth )
        legendText1.grid( row=3, column=0, sticky='w' )
        legendText2.grid( row=4, column=0, sticky='w' )
        legendText3.grid( row=5, column=0, sticky='w' )
        legendText4.grid( row=6, column=0, sticky='w' )

        # Quit button
        quitButton = tkinter.Button( self, text="Exit", borderwidth=0, justify='center', width=len('Start'), command=self.OnExit )
        quitButton.grid( row=4, column=1, sticky='n', rowspan=2 )

        # Game start button
        startButton = tkinter.Button( self, text="Start", borderwidth=0, justify='center', width=len('Start'), command=self.OnStart )
        startButton.grid( row=5, column=1, sticky='s', rowspan=2 )

    def OnInfo(self) :
        infoString = "==Akemi's Word Game v" + GAME_VERSION + "=="
        infoString = infoString + "\n\nThe game where you try and guess"
        infoString = infoString + "\nthe randomly generated word!"
        infoString = infoString + "\n\nGame originally hosted on Github:"
        infoString = infoString + "\nhttps://github.com/dencee/AWG"
        infoString = infoString + "\n\nHave Fun!!!"
        tkinter.messagebox.showinfo( "AWG Info", infoString )

    def OnExit(self) :
        self.destroy()       # So dramatic!

    def OnStart(self) :
        # Get plural option only once when the game starts so the value can't be adjusted mid-game
        self.checkPlurals = self.pluralCheckVal.get()

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

        # Reset the number of guesses that've been made
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
                            resultList.append("\u25b2")    # unicode char for triangle
                        else :
                            resultList.append("O")
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

        # Loop through all words in the dictionary file (SINGLE.TXT) to extract the ones
        # matching the game criteria
        for index, word in enumerate( WordGame_tk.dictWordList ) :        
            if ( len(word) == numLetters ) :
                lettersInWord = dict()
                
                # Loop through all the letters and,
                # 1) check it's a valid lowercase letter
                # 2) count the occurrence of each letter--it's illegal to have a
                # letter occur more than once in a word
                for letter in word :
                    if ( ( letter < 'a' ) or ( letter > 'z' ) ) :
                        # Word can only contain lower-case letters: no pronouns,
                        # apostrophes, accents, etc. stop checking other letters if found
                        break
                    
                    # TODO: Don't really need to keep track of the number of occurrences
                    # since I'm just looking at dictionary length size.
                    lettersInWord[letter] = lettersInWord.get( letter, 0 ) + 1
                
                # Check only 1 instance of each letter:
                # If each letter occurred only once, then the dictionary size will be
                # equal to the length of the word string that was read
                if len(lettersInWord) == len(word) :
                    
                    # 0 = box not checked (include plurals); 1 = box checked (omit plurals)
                    if self.checkPlurals != 0 :                    
                        # Want to determine if this word is a plural so look back in the sorted
                        # dictionary list and grab some of the words before it. If there's
                        # the same word without an 's' or 'es' at the end, this word's a plural
                        if index > 10 :
                            startIndex = ( index - 10 )
                        else :
                            startIndex = 0
                        pastWords = tuple( WordGame_tk.dictWordList[ startIndex : index ] )
                        
                        # Check for plural words ending in 's':
                        # if word ends in an 's' and there's the same word without an 's' at the
                        # end then consider this word a plural. No 100% accurate, but given the
                        # size of the word list file it's acceptable.
                        if ( word[len(word)-1] == 's' ) and ( word[ : (len(word)-1) ] in pastWords ) :
                            continue    # continue, not break--still searching for other words
                        
                        # Check for plural words ending in 'es':
                        # Same for plurals ending in 's'
                        if ( word[ (len(word)-2) : ] == 'es' ) and ( word[ : (len(word)-2) ] in pastWords ) :
                            continue    # continue, not break--still searching for other words
                    
                    # Valid word found...Finally!
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
            
            # Sort the list so it'll be easier to find plurals
            WordGame_tk.dictWordList.sort()


if __name__ == '__main__':
    game = WordGame_tk(None)
    game.title("Akemi's Word Game")
    game.mainloop()
    