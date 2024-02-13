from Core.pieces import *


class Move:
    START_SQUARE = None
    TARGET_SQUARE = None

    def __init__(self, START_SQUARE, TARGET_SQUARE):
        self.START_SQUARE = START_SQUARE
        self.TARGET_SQUARE = TARGET_SQUARE


DIRECTION_OFFSETS = (8, -8, -1, 1, 7, -7, 9, -9)
NUM_SQUARES_TO_EDGE = [None]*64

legalMoves = []


def GenerateMoves(board, color_to_move):
    legalMoves = []

    for startSquare in range(64):
        piece = board[startSquare]
        if piece == None:
            continue
        if IsColor(piece, color_to_move):
            if IsSlidingPiece(piece):
                GenerateSlidingMoves(board, color_to_move, startSquare, piece)
    
def GenerateSlidingMoves(board, color_to_move, startSquare, piece):
    startDirIndex = 4 if IsBishop(piece) else 0
    endDirIndex = 4 if IsRook(piece) else 8

    for directionIndex in range(startDirIndex, endDirIndex):
        for n in range(NUM_SQUARES_TO_EDGE[startSquare][directionIndex]):
            targetSquare = startSquare + DIRECTION_OFFSETS[directionIndex] * (n+1)
            pieceOnTargetSquare = board[targetSquare]

            if pieceOnTargetSquare == None:
                legalMoves.append(Move(startSquare, targetSquare))
                continue

            if IsColor(pieceOnTargetSquare, color_to_move):
                break

            legalMoves.append(Move(startSquare, targetSquare))

            if not IsColor(pieceOnTargetSquare, color_to_move):
                break

def ComputeMoveData():
    for file in range(8):
        for rank in range(8):
            numNorth = 7 - rank
            numSouth = rank
            numWest = file
            numEast = 7 - file

            squareIndex = rank * 8 + file

            NUM_SQUARES_TO_EDGE[squareIndex] = [
                numNorth,
                numSouth,
                numWest,
                numEast,
                min(numNorth, numWest),
                min(numSouth, numEast),
                min(numNorth, numEast),
                min(numSouth, numWest)
            ]