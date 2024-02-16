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
            
            if IsKing(piece):
                GenerateKingMoves(board, color_to_move, startSquare)
            
            if IsKnight(piece):
                GenerateKnightMoves(board, color_to_move, startSquare)

            if IsPawn(piece):
                GeneratePawnMoves(board, color_to_move, startSquare)


def GeneratePawnMoves(board, color_to_move, startSquare):
    startRank = 1 if color_to_move == WHITE else 6
    direction = DIRECTION_OFFSETS[0] if color_to_move == WHITE else DIRECTION_OFFSETS[1]
    captureDirection = (DIRECTION_OFFSETS[4], DIRECTION_OFFSETS[6]) if color_to_move == WHITE else (DIRECTION_OFFSETS[5], DIRECTION_OFFSETS[7])

    currentRank = (startSquare - startSquare % 8) / 8

    # Double move
    if currentRank == startRank:
        targetSquare = startSquare + direction * 2
        pieceOnTargetSquare = board[targetSquare]

        if pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move):
            legalMoves.append(Move(startSquare, targetSquare))
    
    # Regular move
    targetSquare = startSquare + direction
    pieceOnTargetSquare = board[targetSquare]

    if pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move):
        legalMoves.append(Move(startSquare, targetSquare))
    
    # Capture
    for dir in captureDirection:
        targetSquare = startSquare + dir
        pieceOnTargetSquare = board[targetSquare]

        if pieceOnTargetSquare != None and not IsColor(pieceOnTargetSquare, color_to_move):
            legalMoves.append(Move(startSquare, targetSquare))


def GenerateKnightMoves(board, color_to_move, startSquare):
    knightDirectionOffsets = [
        15,
        17,
        6,
        -10,
        10,
        -6,
        -17,
        -15
    ]

    for directionIndex in range(0, 8):
        targetSquare = startSquare + knightDirectionOffsets[directionIndex]

        if targetSquare < 0 or targetSquare > 63:
            continue

        pieceOnTargetSquare = board[targetSquare]

        startSquareColor = ((startSquare % 8) + (7 - (startSquare - startSquare % 8) / 8)) % 2
        targetSquareColor = ((targetSquare % 8) + (7 - (targetSquare - targetSquare % 8) / 8)) % 2
        isSameColorSquare = startSquareColor == targetSquareColor

        if not isSameColorSquare and (pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move)):
            legalMoves.append(Move(startSquare, targetSquare))

def GenerateKingMoves(board, color_to_move, startSquare):
    for directionIndex in range(0, 8):
        targetSquare = startSquare + DIRECTION_OFFSETS[directionIndex]

        if targetSquare < 0 or targetSquare > 63:
            continue

        pieceOnTargetSquare = board[targetSquare]

        if pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move):
            legalMoves.append(Move(startSquare, targetSquare))

    
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