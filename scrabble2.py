from sys import stdin
import math
import sys
import random


TILES_USED = 0 # records how many tiles have been returned to user
CELL_WIDTH = 3 # cell width of the scrabble board
SHUFFLE = False # records whether to shuffle the tiles or not

# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]

# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board

# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s,t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem//2
    s = t*rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t*rem
    return s

# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH*" "
    board_str =  "  |" + "|".join(getString(item," ") for item in range(len(Board)))  +"|"
    line1 = "--|" + "|".join(getString("","-") for item in range(len(Board)))  +"|"

 
    print(board_str)
    print(line1)
    
    for i in range(len(Board)):
        row = str(i) + " "*(2-len(str(i))) +"|"
        for j in range(len(Board)):
            row += getString(Board[i][j]," ") + "|"
        print(row)
        print(line1)
        
    print()

scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter,score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line= line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)


validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")


Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################
# Reading data from dictionary.text
dictionary = open("dictionary.txt", "r")
dictionaryList = []
for line in dictionary:
    line = line.strip()
    dictionaryList.append(line)
dictionary.close()

# create a list of valid English letters
letterList = []
for item in Scores:
    letterList.append(item[0])


# check whether the input word contains valid letters or not
def checkLetter(inputString, checkList):
    for letter in inputString:
        if checkList.count(letter.upper()) == 0:
            return False
    return True


# check whether the input word is in the dictionary or not
def checkWord(inputString, dic):
    for word in dic:
        if inputString.upper() == word:
            return True
    return False


# check whether a word can be made from the new tiles and used tiles or not
def checkUse(inputString, tiles):
    # copy new tiles
    allTiles = 1*tiles
    # copy used tiles on the Board
    for i in Board:
        for j in i:
            if j != "":
                allTiles.append(j)
    for letter in inputString:
        if allTiles.count(letter.upper()) == 0:
            return False
        else:
            allTiles.remove(letter.upper())
    return True


# split the input location from user
def separateString(inputString):
    inputString = inputString.split(":")
    return inputString


# check whether input row and column are in valid range or not
def checkRowCol(inputNumber,boardLen):
    if inputNumber >= 0 and inputNumber <= boardLen:
        return True
    else:
        return False


# check the format of the input location
def checkLocFormat(inputString):
    validFormat = False
    locList = separateString(inputString)
    if len(locList) != 3:
        validFormat = False
    else:
        rowLoc = locList[0]
        colLoc = locList[1]
        dir = locList[2].upper()
        # row and column need to be digits
        if rowLoc.isdigit() and colLoc.isdigit():
            rowLoc = int(rowLoc)
            colLoc = int(colLoc)
            # row and column in correct range
            if checkRowCol(rowLoc, BOARD_SIZE-1) and checkRowCol(colLoc, BOARD_SIZE-1):
                # correct direction format
                if dir == "H" or dir == "V":
                    validFormat = True
    return validFormat


# length of possible words must be equal or shorter than board size
def checkWordLength(word, row, col, direction):
    if direction == "H":
        sumLength = len(word) + col
        if sumLength <= BOARD_SIZE:
            return True
    else:
        sumLength = len(word) + row
        if sumLength <= BOARD_SIZE:
            return True
    return False


# if the letter is being put to an empty tile on the Board, the letter needs to be in myTiles
def checkNewTiles(thisLetter, tiles):
    if thisLetter.upper() in tiles:
        tiles.remove(thisLetter.upper())
        return True
    else:
        return False


# if the letter is being put to a used tile on the Board, the letter must be the same letter on the Board
def checkOldTiles(thisLetter, letterCheck):
    if thisLetter.upper() != letterCheck:
        return False
    else:
        return True


# check whether the new move is valid or not
def checkNewMove(word, first, rowLoc, colLoc, dir):
    # if it is the first move, users dont need to use existing tiles
    useExist = first
    thisTiles = 1*myTiles
    for i in range(len(word)):
        if dir == "H":
            letterCheck = Board[rowLoc][colLoc + i]
        else:
            letterCheck = Board[rowLoc + i][colLoc]

        if letterCheck != "":
            if not checkOldTiles(word[i], letterCheck):
                return False
            else:
                # indicate existing tiles have been used
                useExist = True
        else:
            if not checkNewTiles(word[i], thisTiles):
                return False
        i += 1
    return useExist


# get the first move location for row and column
def getStartLoc(size):
    startLoc = size//2
    return startLoc


# a summarized function that checks all criteria for a new move
def checkValidMove(word, inputString, first):
    # check valid letters and the word is from dictionary
    if not checkLetter(word, letterList) or not checkWord(word, dictionaryList):
        return False

    # check input location format
    if not checkLocFormat(inputString):
        return False
    else:
        # break the input location string into components
        locList = separateString(inputString)
        rowLoc = int(locList[0])
        colLoc = int(locList[1])
        dir = locList[2].upper()
        # if first move
        if first:
            startLoc = getStartLoc(BOARD_SIZE)
            if rowLoc != startLoc or colLoc != startLoc:
                return False
        # check whether word can fit into the board
        if not checkWordLength(word, rowLoc, colLoc, dir):
            return False
        else:
            return checkNewMove(word, first, rowLoc, colLoc, dir)


# get letters from new tiles that should be calculated for a move
def getUsedLetters(word, loc):
    locList = separateString(loc)
    rowLoc = int(locList[0])
    colLoc = int(locList[1])
    dir = locList[2].upper()
    scoreLetters = []
    for i in range(len(word)):
        if dir == "H":
            boardLetter = Board[rowLoc][colLoc + i]
            if boardLetter == "":
                scoreLetters.append(word[i].upper())
        else:
            boardLetter = Board[rowLoc + i][colLoc]
            if boardLetter == "":
                scoreLetters.append(word[i].upper())
        i += 1
    # return a list that will be passed to calculateScore function below
    return scoreLetters


# get the list of used letters and calculate the score for a move
def calculateScore(inputList, scoreList):
    wordScore = 0
    for aLetter in inputList:
        i = 0
        foundLetter = False
        while not foundLetter:
            if aLetter.upper() == scoreList[i][0]:
                wordScore += scoreList[i][1]
                foundLetter = True
            i += 1
    return wordScore


# update board with a valid move, also remove used letters from my tiles
def updateBoard(word, loc):
    locList = separateString(loc)
    rowLoc = int(locList[0])
    colLoc = int(locList[1])
    dir = locList[2].upper()
    for i in range(len(word)):
        if dir == "H":
            boardLetter = Board[rowLoc][colLoc + i]
            if boardLetter == "":
                Board[rowLoc][colLoc + i] = word[i].upper()
                myTiles.remove(word[i].upper())
        else:
            boardLetter = Board[rowLoc + i][colLoc]
            if boardLetter == "":
                Board[rowLoc + i][colLoc] = word[i].upper()
                myTiles.remove(word[i].upper())
        i += 1


# generate all locations based on board_size
def generateAllLoc(size):
    allLoc = []
    for i in range(size):
        for j in range(size):
            for k in ["H", "V"]:
                allLoc.append([i, j, k])
    return allLoc


# generate all possible words that can fit into the board
def findValidWords(size, dictionary, first):
    validWords = []
    firstSize = getStartLoc(size)
    for word in dictionary:
        # if it is the first move, word length is halved
        if first:
            if len(word) + firstSize <= size and checkUse(word, myTiles):
                validWords.append(word)
        else:
            if len(word) <= size and checkUse(word, myTiles):
                validWords.append(word)
    return validWords


# generate possible locations for a single word
def generatePosLoc(word, locList):
    posLoc = []
    wordLength = len(word)
    for item in locList:
        if item[2] == "H":
            if item[1] + wordLength <= BOARD_SIZE:
                posLoc.append(item)
        else:
            if item[0] + wordLength <= BOARD_SIZE:
                posLoc.append(item)
    return posLoc


# generate all possible moves based on the current board
def findAllMoves(size, dictionary, locList, first):
    # all moves are stored in allMoves list
    allMoves = []
    # list of valid words based solely on the length of the word
    validWords = findValidWords(size, dictionary, first)
    # loop through every possible word
    for item in validWords:
        # if it is the first move, there are only 2 possible locations
        firstLoc = getStartLoc(BOARD_SIZE)
        if first:
            posLoc = [[firstLoc, firstLoc, "H"], [firstLoc, firstLoc, "V"]]
        # if it is NOT the first move, generatePosLoc functions will generate all possible locations (based on word length) for the current word in the loop
        else:
            posLoc = generatePosLoc(item, locList)
        # loop through all possible locations to check whether it is a valid move or not
        for loc in posLoc:
            rowLoc = loc[0]
            colLoc = loc[1]
            dir = loc[2]
            locString = str(rowLoc) + ":" + str(colLoc) + ":" + dir
            # if valid, the score of this move is calculated and the move is appended to allMoves list
            if checkNewMove(item, first, rowLoc, colLoc, dir):
                thisScore = calculateScore(getUsedLetters(item, locString), Scores)
                allMoves.append([item, locString, thisScore])
    return allMoves


# find max score in a list
def findMax(moveList):
    maxScore = 0
    for item in moveList:
        if item[2] > maxScore:
            maxScore = item[2]
    return maxScore


# get all moves with the max score
def findPosMax(moveList, score):
    posList = []
    for item in moveList:
        if item[2] == score:
            posList.append(item)
    return posList


# GAME STARTS HERE
# set firstMove to true at the start of the game, also generate all locations based on board size
firstMove = True
allLoc = generateAllLoc(BOARD_SIZE)
inputWord = input("Please enter a word: ")
totalScore = 0

while inputWord != "***":
    inputLoc = input("Enter the location in row:col:direction format: ")
    while not checkValidMove(inputWord, inputLoc, firstMove) and inputWord !="***":
        # print appropriate feedback if it is the first move
        if firstMove:
            startPosLoc = getStartLoc(BOARD_SIZE)
            startLoc1 = str(startPosLoc) + ":" + str(startPosLoc) + ":" + "H"
            startLoc2 = str(startPosLoc) + ":" + str(startPosLoc) + ":" + "V"
            print("The location in the first move must be " + startLoc1 + " or "+startLoc2)
        # print invalid move
        print("Invalid Move!!!")
        print("")
        inputWord = input("Please enter a word: ")
        if inputWord != "***":
            inputLoc = input("Enter the location in row:col:direction format: ")
    if inputWord != "***":
        # find the maximum score for this turn
        allMove = findAllMoves(BOARD_SIZE, dictionaryList, allLoc, firstMove)
        maxScoreMove = findPosMax(allMove, findMax(allMove))
        # print(maxScoreMove)
        # calculate user move score
        scoreLetters = getUsedLetters(inputWord, inputLoc)
        thisTurnScore = calculateScore(scoreLetters, Scores)
        # if user score = max score, say this
        if thisTurnScore == maxScoreMove[0][2]:
            print("Your move was the best move. Well done!")
        print("Maximum possible score in this move was " + str(maxScoreMove[0][2]) + " with word "+maxScoreMove[0][0]+" at " +maxScoreMove[0][1])
        print("This turn score is: " + str(thisTurnScore))
        totalScore += thisTurnScore
        print("Total score is: " + str(totalScore))
        updateBoard(inputWord, inputLoc)
        printBoard(Board)
        firstMove = False
        getTiles(myTiles)
        printTiles(myTiles)
        inputWord = input("Please enter a word: ")
print("")
print("Game ended")