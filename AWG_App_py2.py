# Title:  AWG - Akemi's Word Game
# Author: Daniel Commins 
# Date:   June 13, 2015
# Files:  AWG_App_py2.py; SINGLE.TXT (dictionary words file)
# Tested: python 2.61
# Info:   Akemi's Word Game: The game where you try and guess the computer's randomly
#         selected word! Each letter appears only once.

import sys
import random
import Tkinter
import tkMessageBox

GAME_VERSION = "1.3"

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

class WordGame_tk( Tkinter.Tk ) :
    entryWidth = 30         # in chars
    guessStartRow = 8       # using grid()
    dictWordListEasy = None # only needs to be read once for all instances
    dictWordListHard = None # only needs to be read once for all instances

    def __init__( self, parent ):
        Tkinter.Tk.__init__(self, parent)
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
        self.statusText = Tkinter.StringVar()   # string message on the status line
        self.statusLabel = None                 # status label widget
        self.randomWord = None                  # randomly selected word from dictionary
        self.wordList = list()                  # stores words from dictionary of the specified length
        self.pluralCheckVal = Tkinter.IntVar()  # stores value from user option to include word plurals
        self.exSpacesCheckVal = Tkinter.IntVar()# stores value from user option to include extra spaces in result
        self.difficultyVal = Tkinter.IntVar()   # stores the game difficulty level
        self.checkPlurals = None                # stores the plural check option when game starts
        self.extraSpaces = None                 # stores the option to add a space every character in result
        self.difficulty = None                  # stores the game difficulty level when the game starts

        # Open and read large words file once if necessary
        self.ReadWordsFile()

        # Set grid geometry
        self.grid()

        # Plural checkbox; enable by default
        pluralCheckButton = Tkinter.Checkbutton( self, text="omit 's'/'es' plurals", variable=self.pluralCheckVal, onvalue=1, offvalue=0 )
        pluralCheckButton.grid( row=0, column=0, sticky='w' )
        pluralCheckButton.select()
        
        # Extra spaces checkbox; disable by default
        extraSpacesCheckButton = Tkinter.Checkbutton( self, text="extra spaces", variable=self.exSpacesCheckVal, onvalue=1, offvalue=0 )
        extraSpacesCheckButton.grid( row=0, column=0, sticky='e' )
        extraSpacesCheckButton.deselect()
        
        # Info button 
        infoButton = Tkinter.Button( self, text="Info", borderwidth=0, justify='center', command=self.OnInfo )
        infoButton.grid( row=0, column=1, sticky='n', rowspan=1 )
        
        # Game difficulty level radio buttons
        radioButton = Tkinter.Radiobutton( self, text="Easy", variable=self.difficultyVal, value=0 )
        radioButton.grid( row=1, column=0, sticky='w' )
        radioButton = Tkinter.Radiobutton( self, text="Hard", variable=self.difficultyVal, value=2)
        radioButton.grid( row=1, column=0, sticky='' )

        # Number of letters option
        lettersText = Tkinter.Label( self, anchor='w', text="Number of Letters [%d-%d]" %(self.minLetters, self.maxLetters) )
        lettersText.grid( row=2, column=0, sticky='w' )

        self.lettersEntry = Tkinter.Spinbox( self, from_=self.minLetters, to=self.maxLetters, width=3 )
        self.lettersEntry.grid( row=2, column=1, sticky='w' )
        self.lettersEntry.delete( 0, 3 )
        self.lettersEntry.insert( 0, '5' )

        # Number of guesses option
        numGuessesText = Tkinter.Label( self, anchor="w", text="Number of Guesses [1-%d]" %(self.maxAttempts) )
        numGuessesText.grid( row=3, column=0, sticky='w' )

        self.guessesEntry = Tkinter.Spinbox( self, from_="1", to=self.maxAttempts, width=3 )
        self.guessesEntry.grid( row=3, column=1, sticky='w' )
        self.guessesEntry.delete( 0, 3 )
        self.guessesEntry.insert( 0, '5' )

        # Statement of rules
        legendText1 = Tkinter.Label( self, anchor='center', text="*Each letter is used only once*", borderwidth=0, bg='yellow', padx=4, width=WordGame_tk.entryWidth )
        legendText2 = Tkinter.Label( self, anchor='w', text="O = right letter, wrong location", borderwidth=0, bg='cyan', padx=4, width=WordGame_tk.entryWidth )
        legendText3 = Tkinter.Label( self, anchor='w', text=u"\u25b2 = right letter, right location", borderwidth=0, bg='green', padx=4, width=WordGame_tk.entryWidth )
        legendText4 = Tkinter.Label( self, anchor='w', text="_ = letter not in word", borderwidth=0, bg='red', padx=4, width=WordGame_tk.entryWidth )
        legendText1.grid( row=4, column=0, sticky='w' )
        legendText2.grid( row=5, column=0, sticky='w' )
        legendText3.grid( row=6, column=0, sticky='w' )
        legendText4.grid( row=7, column=0, sticky='w' )

        # Quit button
        quitButton = Tkinter.Button( self, text="Exit", borderwidth=0, justify='center', width=len('Start'), command=self.OnExit )
        quitButton.grid( row=5, column=1, sticky='n', rowspan=2 )

        # Game start button
        startButton = Tkinter.Button( self, text="Start", borderwidth=0, justify='center', width=len('Start'), command=self.OnStart )
        startButton.grid( row=6, column=1, sticky='s', rowspan=2 )

    def OnInfo(self) :
        infoString = "==Akemi's Word Game v" + GAME_VERSION + "=="
        infoString = infoString + "\n\nThe game where you try and guess"
        infoString = infoString + "\nthe randomly generated word!"
        infoString = infoString + "\n\nGame originally hosted on Github:"
        infoString = infoString + "\nhttps://github.com/dencee/AWG"
        infoString = infoString + "\n\nHave Fun!!!"
        tkMessageBox.showinfo( "AWG Info", infoString )

    def OnExit(self) :
        self.destroy()       # So dramatic!

    def OnStart(self) :
        # Get plural option only once when the game starts so the value can't be adjusted mid-game
        self.checkPlurals = self.pluralCheckVal.get()

        # Get extra spaces option
        self.extraSpaces = self.exSpacesCheckVal.get()
        
        # Get the game difficulty
        self.difficulty = self.difficultyVal.get()

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
            if ( self.difficulty == 0 ) :
                self.randomWord = self.GetRandomWord( WordGame_tk.dictWordListEasy, self.numLetters )
            else :
                self.randomWord = self.GetRandomWord( WordGame_tk.dictWordListHard, self.numLetters )

        # Reset the number of guesses that've been made
        self.curGuessNum = 0
        
        startRow = WordGame_tk.guessStartRow

        # Print status label if necessary
        if self.statusLabel == None :
            self.statusLabel = Tkinter.Label( self, textvariable=self.statusText, borderwidth=0, width=WordGame_tk.entryWidth )
            self.statusLabel.grid( row=startRow, column=0 )
        else :
            self.statusLabel.grid()
        self.statusText.set( statusText )

        startRow = ( startRow + 1 )

        # Print user guess entry field if necessary
        if self.numLetters != None :
            if self.curGuess.entry == None :
                self.curGuess.entry = Tkinter.Entry( self, borderwidth=0, width=WordGame_tk.entryWidth, bg='gray80', state='normal' )
                self.curGuess.entry.insert( 0, "<Enter Guess>" )
                self.curGuess.entry.grid( row=startRow, column=0 )
            else :
                self.curGuess.entry.grid()
                self.curGuess.entry.delete( 0, 'end' )
            
        # Print the user guess button if necessary
        if self.numLetters != None :
            if self.curGuess.button == None :
                self.curGuess.button = Tkinter.Button( self, text="Guess", borderwidth=0, justify='center', width=len('Start'), command=self.OnGuess )        
                self.curGuess.button.grid( row=startRow-1, column=1, sticky='s', rowspan=2 ) # -1 because rowspan=2
            else :
                self.curGuess.button.grid()
            
        startRow = ( startRow + 1 )

        # First time 'Start' is pressed, create all the guess entries and leave them blank
        # TODO: Possibly reverse the if and for statements
        if self.guesses[0].pastGuess == None :
            for eachGuess in range( self.maxAttempts ) :
                self.guesses[eachGuess].guess = Tkinter.StringVar()
                self.guesses[eachGuess].matches = Tkinter.StringVar()
                self.guesses[eachGuess].guess.set( "" )
                self.guesses[eachGuess].matches.set( "" )
                
                self.guesses[eachGuess].pastGuess = Tkinter.Label( self, textvariable=self.guesses[eachGuess].guess, borderwidth=0, anchor='w', width=WordGame_tk.entryWidth )
                self.guesses[eachGuess].result = Tkinter.Label( self, textvariable=self.guesses[eachGuess].matches, borderwidth=0, anchor='w', width=WordGame_tk.entryWidth )
                
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
            # Note - want to allow repeating letters because user may be trying to guess
            # the location of one of the letters
            invalidLetter = False
            for letter in userGuess :
                if ( ( letter < 'a' ) or ( letter > 'z' ) ) :
                    invalidLetter = True
                    break
                
            # Check valid symbols
            if invalidLetter == True :
                self.statusText.set( "Error: Invalid symbols in word" )  
            else :
                # Valid entry! Check letter matches with the random word
                resultList = list()
                wrongLetters = 0
                
                # Loop letters in guess word, checking letter in word, then correct position
                for index, letter in enumerate( userGuess ) :
                    if letter in self.randomWord :
                        if ( userGuess[index] == self.randomWord[index] ) :
                            resultList.append(u"\u25b2")    # unicode char for triangle
                        else :
                            resultList.append("O")
                            wrongLetters = wrongLetters + 1
                    else :
                        resultList.append("_")
                        wrongLetters = wrongLetters + 1
                        
                    if self.extraSpaces != 0 :
                        # Skip space every character for readability
                        if len( resultList ) != 0 :
                            resultList.append(" ")

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
        for index, word in enumerate( listOfWords ) :
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
                        pastWords = tuple( listOfWords[ startIndex : index ] )
                        
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
        if ( WordGame_tk.dictWordListEasy == None ) :
            fileHandle = None
            wordFile = "EASY.TXT"

            # 'with' statement will automatically close the file afterwards
            with open(wordFile) as fileHandle :
                # Populate list with all words read from file
                WordGame_tk.dictWordListEasy = fileHandle.read().splitlines()
            
                # Sort the list so it'll be easier to find plurals
                WordGame_tk.dictWordListEasy.sort()

        # Only need to be read once
        if ( WordGame_tk.dictWordListHard == None ) :
            fileHandle = None
            wordFile = "HARD.TXT"

            # 'with' statement will automatically close the file afterwards
            with open(wordFile) as fileHandle :
                # Populate list with all words read from file
                WordGame_tk.dictWordListHard = fileHandle.read().splitlines()
            
                # Sort the list so it'll be easier to find plurals
                WordGame_tk.dictWordListHard.sort()


if __name__ == '__main__':
    game = WordGame_tk(None)
    game.title("Akemi's Word Game")
    game.mainloop()
    