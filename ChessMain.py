"""
Main Driver file . Handling User Input and displaying current game state object.
"""

import pygame as p
import ChessEngine, SmartMoveFinder

# from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 1000
IMAGES = {}


def loadImages():
    pieces = ["wp", "wN", "wB", "wK", "wQ", "wR", "bp", "bN", "bB", "bR", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# WE can access an image by saying 'IMAGES['wp']'

"""
The main driver of our code. This will handle input and updating the graphics.
"""


def main():
    global returnQueue
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 12, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()

    moveMade = False

    loadImages()
    running = True

    sqSelected = ()
    playerClicks = []

    playerOne = True  # if human is white it is true , if AI is white the false.
    playerTwo = False  # same but for black

    # AIThinking = False
    # moveFinderProcess = None
    gameOver = False
    moveUndone = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # ( x, y ) location
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row, col) or col >= 8:  # user clicked same location twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2 and humanTurn:  # after second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                    # if AIThinking:
                    # moveFinderProcess.terminate()
                    # AIThinking = False
                    moveUndone = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
                    # if AIThinking:
                    # moveFinderProcess.terminate()
                    # AIThinking = False
                    moveUndone = True
        if not humanTurn and not gameOver and not moveUndone:
            # if not AIThinking:
            # AIThinking = True
            # print("thinking...")
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)  # , returnQueue)
            # returnQueue = Queue()
            # moveFinderProcess = Process(target=SmartMoveFinder.findBestMoveMinMax, args=(gs, validMoves, returnQueue))
            # moveFinderProcess.start()

            # if not moveFinderProcess.is_alive():
            # print("done thinking")
            # AIMove = returnQueue.get()
            # TAB below
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            # AIThinking = False

        if moveMade:
            validMoves = gs.getValidMoves()

            moveMade = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            drawEndGameText(screen,
                            "Stalemate" if gs.staleMate else "Black wins by Checkmate" if gs.whiteToMove else "White wins by Checkmate")
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # draws squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("light blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("dark green"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog)):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1])
        moveTexts.append(moveString)
    padding = 5
    lineSpacing = 2
    textY = padding
    textY2 = padding
    textY3 = padding
    for i in range(0, len(moveLog), 2):
        if i < 62:
            text = moveTexts[i]
            textObject = font.render(text, True, p.Color("White"))
            textLocation = moveLogRect.move(padding, textY)
            screen.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing
        if 62 <= i < 124:
            text = moveTexts[i]
            textObject = font.render(text, True, p.Color("White"))
            textLocation = moveLogRect.move(padding + 70, textY2)
            screen.blit(textObject, textLocation)
            textY2 += textObject.get_height() + lineSpacing

        if i >= 124:
            text = moveTexts[i]
            textObject = font.render(text, True, p.Color("White"))
            textLocation = moveLogRect.move(padding + 140, textY3)
            screen.blit(textObject, textLocation)
            textY3 += textObject.get_height() + lineSpacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, False, p.Color("Black"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color("Gray"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
