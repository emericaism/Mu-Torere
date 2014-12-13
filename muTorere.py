import math
import random
import numpy as np


#we create the network of legal edges
global edgeNetwork
edgeNetwork = [[0,1,0,1,1,0,0,0,0],
               [1,0,1,0,1,0,0,0,0],
               [0,1,0,0,1,1,0,0,0],
               [1,0,0,0,1,0,1,0,0],
               [1,1,1,1,0,1,1,1,1],
               [0,0,1,0,1,0,0,0,1],
               [0,0,0,1,1,0,0,1,0],
               [0,0,0,0,1,0,1,0,1],
               [0,0,0,0,1,1,0,1,0]]

global startingOccupancies
startingOccupancies = ['B','B','B','B','O','W','W','W','W']



def printBoard(listOfOccupancies=list):
    print str(listOfOccupancies[0])+"-"+str(listOfOccupancies[1])+"-"+str(listOfOccupancies[2])
    print "|\\|/|"
    print str(listOfOccupancies[3])+"-"+str(listOfOccupancies[4])+"-"+str(listOfOccupancies[5])
    print "|/|\\|"
    print str(listOfOccupancies[6])+"-"+str(listOfOccupancies[7])+"-"+str(listOfOccupancies[8])

def ShowLegalMoves(listOfOccupancies=list,colorToPlay=str):
    if colorToPlay=='B':
        notColor = 'W'
    elif colorToPlay=='W':
        notColor = 'B'
    openNode = listOfOccupancies.index('O')
    edgesList = edgeNetwork[openNode]
    NodesWithExistingEdges = [i for i, x in enumerate(edgesList) if x == 1]
    #putahi
    piecesToMove = []
    if openNode == 4:
        for node in NodesWithExistingEdges:
            if listOfOccupancies[node] == colorToPlay:
                AdjacentNodes = []
                edgesList2 = edgeNetwork[node]
                NodesWithExistingEdges2 = [i for i, x in enumerate(edgesList2) if x == 1]
                for node2 in NodesWithExistingEdges2:
                    if listOfOccupancies[node2] == notColor:
                        piecesToMove.append(node)
                        break
    else:
        for node in NodesWithExistingEdges:
            if listOfOccupancies[node] == colorToPlay:
                piecesToMove.append(node)

    #printBoard(listOfOccupancies)
    #print piecesToMove,colorToPlay
    return piecesToMove

def isThereAWinningMove(legalMoves,listOfOccupancies,colorToPlay):
    for move in legalMoves:
        result = makeMove(move,listOfOccupancies,colorToPlay)
        if len(ShowLegalMoves(result,changeColor(colorToPlay))) == 0:
            #then yes, move is a winning move
            return move
    return -1

def makeMove(move=int,listOfOccupancies=list,colorToPlay=str):
    openNode = listOfOccupancies.index('O')
    listOfOccupancies[openNode] = colorToPlay
    listOfOccupancies[move] = 'O'
    return listOfOccupancies

def makeRandomMove(piecesToMove=list,listOfOccupancies=list,colorToPlay=str):
    m = random.choice(piecesToMove)
    return makeMove(m,listOfOccupancies,colorToPlay), m

def makeSmartMove(listOfOccupancies=list,colorToPlay=str, depth=1):
    for x in range(depth):
        legalMoves = ShowLegalMoves(listOfOccupancies,colorToPlay)
        winningMove = isThereAWinningMove(legalMoves,listOfOccupancies,colorToPlay)
        if not winningMove == -1:
            #yes, there's a winning move
            return makeMove(winningMove,listOfOccupancies,colorToPlay)
        else:
            if len(legalMoves)>1:
                for m in legalMoves:
                    listOfOccupancies2 = makeMove(m,listOfOccupancies,colorToPlay)
                    colorToPlay2 = changeColor(colorToPlay)
                    winningMove2 = isThereAWinningMove(ShowLegalMoves(listOfOccupancies,colorToPlay2))
                    if not winningMove == -1:
                        return makeMove(winningMove2,listOfOccupancies,colorToPlay2)
            else:
                return makeMove(legalMoves[0],listOfOccupancies,colorToPlay)

def makeEvaluatedMove(legalMoves,listOfOccupancies,colorToPlay):
    for m in legalMoves:
        evaluated = []
        listOfOccupancies2 = makeMove(m,listOfOccupancies,colorToPlay)
        colorToPlay2 = changeColor(colorToPlay)
        evaluated.append(evaluate(listOfOccupancies2,colorToPlay2))
    miniMoveVal = min(evaluated)
    miniMove = legalMoves[evaluated.index(miniMoveVal)]
    print miniMove
    return makeMove(miniMove,listOfOccupancies,colorToPlay)


def evaluate(listOfOccupancies,colorToPlay):
    value = 0
    #Heuristic 1, occupy center
    if listOfOccupancies[4] == colorToPlay:
        value+=4
    #heuristic 2, have 2 legal moves
    if ShowLegalMoves(listOfOccupancies,colorToPlay) == 2:
        value+=1
    #heuristic 3, reduce clusters
    for i in range(len(listOfOccupancies)):
        if listOfOccupancies[i] == colorToPlay:
            for j in range(len(edgeNetwork[i])):
                if j == 4:
                    continue
                if edgeNetwork[i][j] == 1 and listOfOccupancies[j] == colorToPlay:
                    value-=0.5
                    for k in range(len(edgeNetwork[j])):
                        if k==4 or k==i:
                            continue
                        if edgeNetwork[j][k] == 1 and listOfOccupancies[k] == colorToPlay:
                            value-=1
        if listOfOccupancies[i] == changeColor(colorToPlay):
            for j in range(len(edgeNetwork[i])):
                if j==4:
                    continue
                if edgeNetwork[i][j] == 1 and listOfOccupancies[j] == changeColor(colorToPlay):
                    value+=0.5
                    for k in range(len(edgeNetwork[j])):
                        if k==4 or k==i:
                            continue
                        if edgeNetwork[j][k] == 1 and listOfOccupancies[k] == changeColor(colorToPlay):
                            value+=1
    if len(ShowLegalMoves(listOfOccupancies,colorToPlay)) == 0:
        value = -1000
    return value

def changeColor(toPlay):
    if toPlay=='B':
        notColor = 'W'
    elif toPlay=='W':
        notColor = 'B'
    toPlay = notColor
    return notColor

def playRandomGameSmartish(depth=0):
    totalMoves = 0
    toPlayV = 'W'
    piecesToMoveV = [5,6]
    occupanciesV = ['B','B','B','B','O','W','W','W','W']
    while len(piecesToMoveV)>0:
        printBoard(occupanciesV)
        piecesToMoveV = ShowLegalMoves(occupanciesV,toPlayV)
        print evaluate(occupanciesV,toPlayV)
        print piecesToMoveV,toPlayV
        print "\n"
        if len(piecesToMoveV)==0:
            break
        winningMove = isThereAWinningMove(piecesToMoveV,occupanciesV,toPlayV)
        if winningMove != -1:
            occupanciesV = makeMove(winningMove,occupanciesV,toPlayV)
        else:
            
            occupanciesV = makeEvaluatedMove(piecesToMoveV,occupanciesV,toPlayV)
            print occupanciesV
            #occupanciesV = makeRandomMove(piecesToMoveV,occupanciesV,toPlayV)[0]
        totalMoves+=1
        toPlayV = changeColor(toPlayV)

    print toPlayV + " Loses!"
    print "The game lasted " + str(totalMoves) + " moves."
    return totalMoves

def playRandomGame():
    totalMoves = 0
    toPlayV = 'W'
    piecesToMoveV = [5,6]
    occupanciesV = ['B','B','B','B','O','W','W','W','W']
    while len(piecesToMoveV)>0:
        printBoard(occupanciesV)
        piecesToMoveV = ShowLegalMoves(occupanciesV,toPlayV)
        print "\n"
        if len(piecesToMoveV)==0:
            break
        occupanciesV = makeRandomMove(piecesToMoveV,occupanciesV,toPlayV)[0]
        totalMoves+=1
        toPlayV = changeColor(toPlayV)

    print toPlayV + " Loses!"
    print "The game lasted " + str(totalMoves) + " moves."
    return totalMoves

def humanVsComputer():
    gameLog = []
    totalMoves = 1
    toPlayV = 'W'
    piecesToMoveV = [5,6]
    occupanciesV = ['B','B','B','B','O','W','W','W','W']
    while len(piecesToMoveV)>0:
        printBoard(occupanciesV)
        piecesToMoveV = ShowLegalMoves(occupanciesV,toPlayV)
        print "\n"
        if len(piecesToMoveV)==0:
            break
        if toPlayV == 'W':
            Legal = False
            while not Legal:
                myMove = input(str(totalMoves) + '. ')
                if myMove in piecesToMoveV:
                    Legal=True
            occupanciesV = makeMove(myMove,occupanciesV,toPlayV)
            gameLog.append(myMove)
        elif toPlayV == 'B':
            occupanciesV, m1 = makeRandomMove(piecesToMoveV,occupanciesV,toPlayV)
            gameLog.append(m1)
            totalMoves+=1
        toPlayV = changeColor(toPlayV)

    print toPlayV + " Loses!"
    print "The game lasted " + str(totalMoves) + " moves."
    print gameLog

lengths = []
lengths2 = []
for i in range(10):
    playRandomGameSmartish()

#humanVsComputer()