import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "N": 3, "B": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
secondmovelist = []


whiteKnightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 2, 2, 3, 3, 2, 2, 1],
                     [1, 3, 4, 3, 3, 4, 3, 1],
                     [1, 2, 3, 5, 5, 3, 2, 1],
                     [3, 2, 3, 5, 5, 3, 2, 3],
                     [1, 3, 4, 3, 3, 4, 3, 1],
                     [1, 2, 2, 3, 3, 3, 2, 1],
                     [1, 1, 2, 1, 1, 2, 1, 1]]

blackKnightScores = [[1, 1, 2, 1, 1, 2, 1, 1],
                     [1, 2, 2, 3, 3, 3, 2, 1],
                     [1, 3, 4, 3, 3, 4, 3, 1],
                     [3, 2, 3, 5, 5, 3, 2, 3],
                     [1, 2, 3, 5, 5, 3, 2, 1],
                     [1, 3, 4, 3, 3, 4, 3, 1],
                     [1, 2, 2, 3, 3, 2, 2, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1]]

whiteBishopScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 3, 2, 2, 3, 2, 2],
                     [3, 3, 4, 3, 3, 4, 3, 3],
                     [1, 5, 3, 3, 3, 3, 5, 1],
                     [3, 2, 3, 3, 3, 4, 2, 3],
                     [2, 3, 4, 3, 3, 4, 3, 2],
                     [3, 4, 3, 2, 2, 3, 4, 3],
                     [4, 3, 2, 1, 1, 2, 3, 4]]

blackBishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                     [3, 4, 3, 2, 2, 3, 4, 3],
                     [2, 3, 4, 3, 3, 4, 3, 2],
                     [3, 2, 3, 3, 3, 4, 2, 3],
                     [1, 5, 3, 3, 3, 3, 5, 1],
                     [3, 3, 4, 3, 3, 4, 3, 3],
                     [2, 2, 3, 2, 2, 3, 2, 2],
                     [1, 1, 1, 1, 1, 1, 1, 1]]

whiteQueenScores = [[2, 2, 2, 3, 3, 2, 2, 2],
                    [2, 2, 3, 3, 3, 2, 2, 2],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [1, 2, 3, 3, 3, 2, 2, 1],
                    [4, 2, 3, 3, 3, 2, 2, 3],
                    [1, 6, 3, 3, 3, 4, 4, 1],
                    [1, 2, 5, 4, 4, 1, 2, 1],
                    [1, 1, 1, 3, 3, 1, 1, 1]]

blackQueenScores = [[1, 1, 1, 3, 3, 1, 1, 1],
                    [1, 2, 5, 4, 4, 1, 2, 1],
                    [1, 6, 3, 3, 3, 4, 4, 1],
                    [4, 2, 3, 3, 3, 2, 2, 3],
                    [1, 2, 3, 3, 3, 2, 2, 1],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [2, 2, 3, 3, 3, 2, 2, 2],
                    [2, 2, 2, 3, 3, 2, 2, 2]]

whiteRookScores = [[4, 4, 4, 4, 4, 4, 4, 4],
                   [6, 6, 6, 6, 6, 6, 6, 6],
                   [3, 3, 3, 3, 3, 3, 3, 3],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [1, 1, 3, 3, 3, 1, 3, 3],
                   [4, 4, 4, 4, 4, 4, 4, 4],
                   [4, 3, 4, 4, 4, 4, 3, 4]]

blackRookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
                   [4, 4, 4, 4, 4, 4, 4, 4],
                   [1, 1, 3, 3, 3, 1, 3, 3],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 2, 2, 2, 2],
                   [3, 3, 3, 3, 3, 3, 3, 3],
                   [6, 6, 6, 6, 6, 6, 6, 6],
                   [4, 4, 4, 4, 4, 4, 4, 4]]

whitePawnScores = [[90, 90, 90, 90, 90, 90, 90, 90],
                   [30, 30, 30, 30, 30, 30, 30, 30],
                   [10, 10, 10, 15, 15, 10, 10, 10],
                   [4, 4, 5, 8, 8, 5, 4, 4],
                   [3, 2, 5, 6, 6, 3, 2, 3],
                   [1, 2, 2, 3, 3, 2, 2, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 2, 2, 3, 3, 2, 2, 1],
                   [3, 2, 5, 6, 6, 3, 2, 3],
                   [4, 4, 5, 8, 8, 5, 4, 4],
                   [10, 10, 10, 15, 15, 10, 10, 10],
                   [30, 30, 30, 30, 30, 30, 30, 30],
                   [90, 90, 90, 90, 90, 90, 90, 90]]

whiteKingScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 6, 6, 0, 0, 0, 6, 0]]

blackKingScores = [[0, 6, 6, 0, 0, 0, 6, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

piecePositionScores = {"wN": whiteKnightScores, "wK": whiteKingScores, "wQ": whiteQueenScores, "wR": whiteRookScores,
                       "wB": blackBishopScores, "bB": whiteBishopScores, "bQ": blackQueenScores, "bR": blackRookScores,
                       "bp": blackPawnScores, "wp": whitePawnScores, "bN": blackKnightScores, "bK": blackKingScores}


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# Find best move based on material
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None
    #random.shuffle(validMoves)
    for playerMove in validMoves:
        print(playerMove)
        gs.makeMove(playerMove)
        opponentsMove = gs.getValidMoves()

        if gs.staleMate:
            opponentsMaxScore = STALEMATE
        elif gs.checkMate:
            opponentsMaxScore = - CHECKMATE

        else:
            opponentsMaxScore = - CHECKMATE
            for opponentsMove in opponentsMove:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()

                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                gs.undoMove()
        if opponentsMaxScore < opponentsMinMaxScore:
            opponentsMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove

        gs.undoMove()
    return bestPlayerMove


def findBestMoveMinMax(gs, validMoves):
    global nextMove, counter, move_2

    counter = 0
    nextMove = None
    #random.shuffle(validMoves)
    if len(gs.moveLog) < 2:
        move_2 = None

    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH,  1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #move_2 = secondmovelist[1]
    #print(move_2)
    #print(secondmovelist)
    print(counter)
    # returnQueue.put(nextMove)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove, counter
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE

        for playermove1 in gs.getValidMoves():

            gs.makeMove(playermove1)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = playermove1
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for playermove in gs.getValidMoves():
            gs.makeMove(playermove)
            nextMoves = gs.getValidMoves
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = playermove
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter, move_2
    counter += 1

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        """if move_2 in validMoves:
            gs.makeMove(move_2)
            print("tt")
            nextMoves = gs.getValidMoves()
            score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move, score)
                    print(move_2, score)
                    secondmovelist.insert(0, move)
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break"""

        #else:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
                #print(move_2, score)
                secondmovelist.insert(0, move)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] == "p":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "N":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "K":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "B":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "Q":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "R":
                    piecePositionScore = piecePositionScores[square][row][col]
                # else:
                # piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == "w":
                    score += pieceScore[square[1]] + piecePositionScore * 0.2
                elif square[0] == "b":
                    score -= pieceScore[square[1]] + piecePositionScore * 0.2

    return score


# Score board based on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score
