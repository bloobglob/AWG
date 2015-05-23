// Author: Daniel Commins 
// Date:   May 15, 2015
// Files:  AWG_C.c; SINGLE.TXT (dictionary words file)
// Tested: compiled using...
// Info:   Akemi's Word Game: The game where you try and guess the computer's randomly
//         selected word!

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//#define DEBUG
#define MAX_USER_STRING_CHARS       ( 100 )
#define WORD_FILE                   ( "SINGLE.TXT" )

// Global vars
int gMinLetters = 4;
int gMaxLetters = 12;
int gMaxAttempts = 10;

static char* gpGameTitle = "Akemi's Word Game";
static char wcUserStr[ MAX_USER_STRING_CHARS ] = { 0 };

gListOfReadWords = list()
gWordList = list()

// NOTE - This function isn't thread safe or re-entrant. Just a
// simple function for a simple program
int GetStringFromUser()
{
   unsigned char charIdx;
   char key;
   
   charIdx = 0;
   memset( wcUserStr, 0, sizeof( wcUserStr ) );   
   
   while ( 1 )
   {
      key = getchar();
   
      // Check return key pressed
      if ( ( key == '\r' ) || ( key == '\n' ) ) {
         if ( key == '\r' ) {
            getchar(); // consume the final \n
            wcUserStr[ charIdx ] = '\0';
            charIdx++;
         }
         
         // Exit on return key
         break;
         
      } else {
         // Non-enter key pressed
         wcUserStr[ charIdx ] = key;
         charIdx++;
      }
      
      // Protect against buffer overrun
      if ( charIdx >= MAX_USER_STRING_CHARS ) {
         charIdx = 0
      }
   }   
}

// Pick valid number of words in secret word
int PickNumLetters()
{
   int numLetters = 0;

   while ( 1 ) {
      printf( "Enter the number of letters in secret word [%d-%d]: ", gMinLetters, gMaxLetters );

      // Get num letters from user
      GetStringFromUser();
      numLetters = atoi( wcUserStr );

      if ( numLetters == 0 ) {
         printf( "ERROR: invalid number entered: %s", wcUserStr )
      } else {   
         if ( ( numLetters < gMinLetters ) || ( numLetters > gMaxLetters ) ) {
            printf( "ERROR: enter a number between %d and %d", gMinLetters, gMaxLetters )
         } else {
            // Valid number of letters chosen
            break
         }
      }
   }

   return ( numLetters )
}

int PickNumAttempts()
{
   int numAttempts = 0;
   
   while ( 1 ) {
      printf( "Enter the number of guesses [1-%d]: ", gMaxAttempts );

      // Get num guesses from user
      GetStringFromUser();
      numAttempts = atoi( wcUserStr );

      if ( numAttempts == ) {
         printf( "ERROR: Invalid number of attempts" );
      } else {
         if ( ( numAttempts < 1 ) || ( numAttempts > gMaxAttempts ) ) {
            printf( "ERROR: enter a number between 1 and %d", gMaxAttempts );
         } else {
            // Valid number of letters chosen
            break
         }
      }
   }
   
   return ( numAttempts )
}

const char* GetRandomWord( listOfWords, numLetters )
{
    randomWord = None

    del gWordList[:]

    // Make sure to omit pronouns and words that are the incorrect length
    for word in listOfWords :
        if ( len(word) == numLetters ) :
            if ( ( word[0] >= 'a' ) and ( word[0] <= 'z' ) ) :
                gWordList.append(word)
    
    // Make sure the list is populated with words
    if ( len(gWordList) != 0 ) :
        # Reselect if the same word comes up twice?????
        randomIndex = random.randint( 0, ( len( gWordList ) - 1 ) )
        randomWord = gWordList[ randomIndex ]

    return ( randomWord )

void GetGuessWord( char * const pGuessWord, int chance, int numLetters )
{

   while ( 1 )
   {
      printf( "Guess %d: ", chance );
      GetStringFromUser();
      strcpy( pGuessWord, wcUserStr );
        
      //Check for correct num letters
      if ( strlen( pGuessWord ) != numLetters ) {
            print( "Guess word does not contain %d letters, guess again", numLetters );
      } else {
         int letterIndex;
         int invalidLetter = 0;
         
         for ( letterIndex = 0; letterIndex < strlen( pGuessWord ); letterIndex++ ) {
            if ( ( *( pGuessWord + letterIndex ) < 'a' ) || ( *( pGuessWord + letterIndex ) > 'z' ) ) {
               invalidLetter = 1
               break
            }
            
            if ( invalidLetter != 0 ) {
                printf( "Guess word does not contain all letters, guess again" );
            } else {
               // Valid guess
               break    
            }
         }
      }
   }
            
    return();
}

void OpenWordsFile()
{
   FILE* pFileHandle;
    
   pFileHandle = fopen( WORD_FILE, 'r' );

   if ( pFileHandle == NULL ) {
      print( "ERROR: Unable to open word file: %s", WORD_FILE );
   }

   return ( pFileHandle );
}

int main()
{
   FILE* wordListHandle = NULL;
   changeParams = True            # User has to pick params first time
   int chances = 5;

   // Open and read large words file once
   wordListHandle = OpenWordsFile()
   if ( wordListHandle == NULL ) {
      print( "Unable to open file containing the list of words" );
      return 1;
   }
        
   // Put all words into array
   //gListOfReadWords = wordListHandle.read().splitlines()

   print( "\n-----------------------------------------------------------------------------" );
   print( "Welcome to %s!", gGameTitle );
   print( "Guess at the randomly chosen n-letter word" );
   print( "X = correct letter, wrong location" );
   print( "O = correct letter and location" );
   print( "_ = letter not used in word" );
   // What if a letter is used more than once? Are plurals legal?

   // Main game loop; stay inside until player wants to exit
   while ( 1 )
   {
      resultList = list()

      if ( changeParams != 0 ) :
            # User picks the number of characters in secret word
            numLetters = PickNumLetters()
    
            # User picks the number of attempts at the secret word
            chances = PickNumAttempts()
    
        # Computer picks a random word containing the selected characters
        randomWord = GetRandomWord( gListOfReadWords, numLetters )

        if ( debug != 0 ) :
            print "Random word = ", randomWord
            print "Chances = ", chances
            print "Number of letters = ", numLetters
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
                print "Correct!"
                break
            else :
                #     "Guess %d:"
                print "         " + ''.join(resultList)     # char list to string
        
            chances = chances - 1
   
        if ( chances == 0 ) :
            print "The word was:", randomWord
   
        # Replay????
        replay = GetInput( "Play again? [y=yes; n=no; m=change letters/guesses]" )

        if replay == 'y' :
            changeParams = False
        elif replay == 'm' :
            changeParams = True
        else :
            # Exit game
            break
