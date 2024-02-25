from Core.pieces import *
from Core.boardRepresentation import *
from Core.move import *


class MoveGenerator:
    DIRECTION_OFFSETS = (8, -8, -1, 1, 7, -7, 9, -9)
    NUM_SQUARES_TO_EDGE = [None]*64


    def __init__(self):
        self.legalMoves = []
        self.ComputeMoveData()


    def GenerateLegalMoves(self, board):
        pseudoLegalMoves = self.GenerateMoves(board)
        self.legalMoves = []

        color_to_move = board.color_to_move
        myKingSquare = board.board.index(color_to_move | KING)

        for moveToVerify in pseudoLegalMoves:
            board.MakeMove(moveToVerify, True)
            myKingSquare = board.board.index(color_to_move | KING)

            opponentResponses = self.GenerateMoves(board)

            if not any(response.TARGET_SQUARE == myKingSquare for response in opponentResponses):
                self.legalMoves.append(moveToVerify)
            
            board.UnmakeMove(moveToVerify)

    def GenerateMoves(self, board):
        moves = []

        color_to_move = board.color_to_move

        for startSquare in range(64):
            piece = board.board[startSquare]
            if piece == None:
                continue

            if IsColor(piece, color_to_move):
                if IsSlidingPiece(piece):
                    self.GenerateSlidingMoves(moves, board.board, color_to_move, startSquare, piece)
                
                if IsKing(piece):
                    self.GenerateKingMoves(moves, board, color_to_move, startSquare)
                
                if IsKnight(piece):
                    self.GenerateKnightMoves(moves, board.board, color_to_move, startSquare)

                if IsPawn(piece):
                    self.GeneratePawnMoves(moves, board, color_to_move, startSquare)
        
        return moves


    def GeneratePawnMoves(self, moves, board, color_to_move, startSquare):
        startRank = 1 if color_to_move == WHITE else 6
        direction = self.DIRECTION_OFFSETS[0] if color_to_move == WHITE else self.DIRECTION_OFFSETS[1]
        captureDirection = (self.DIRECTION_OFFSETS[4], self.DIRECTION_OFFSETS[6]) if color_to_move == WHITE else (self.DIRECTION_OFFSETS[5], self.DIRECTION_OFFSETS[7])

        currentRank = (startSquare - startSquare % 8) / 8

        # En passant
        if color_to_move == WHITE:
            if BoardRepresentation.RankIndex(startSquare) == 4:
                if (startSquare+1) in board.doublePawnMoves:
                    if board.board[startSquare+9] == None:
                        enPassantMove = Move(startSquare, startSquare+9)
                        enPassantMove.FLAG = Move.EN_PASSANT
                        moves.append(enPassantMove)

                elif (startSquare-1) in board.doublePawnMoves:
                    if board.board[startSquare+7] == None:
                        enPassantMove = Move(startSquare, startSquare+7)
                        enPassantMove.FLAG = Move.EN_PASSANT
                        moves.append(enPassantMove)
        
        elif color_to_move == BLACK:
            if BoardRepresentation.RankIndex(startSquare) == 3:
                if (startSquare+1) in board.doublePawnMoves:
                    if board.board[startSquare-9] == None:
                        enPassantMove = Move(startSquare, startSquare-9)
                        enPassantMove.FLAG = Move.EN_PASSANT
                        moves.append(enPassantMove)

                elif (startSquare-1) in board.doublePawnMoves:
                    if board.board[startSquare-7] == None:
                        enPassantMove = Move(startSquare, startSquare-7)
                        enPassantMove.FLAG = Move.EN_PASSANT
                        moves.append(enPassantMove)

        # Double move
        if currentRank == startRank:
            targetSquare = startSquare + direction * 2
            pieceOnTargetSquare = board.board[targetSquare]

            if pieceOnTargetSquare == None:
                doubleMove = Move(startSquare, targetSquare)
                doubleMove.FLAG = Move.DOUBLE_PAWN_MOVE
                moves.append(doubleMove)
        
        # Regular move
        targetSquare = startSquare + direction
        pieceOnTargetSquare = board.board[targetSquare]

        if pieceOnTargetSquare == None:
            move = Move(startSquare, targetSquare)
            # Promotion
            if BoardRepresentation.RankIndex(targetSquare) == 7 or BoardRepresentation.RankIndex(targetSquare) == 0:
                move.FLAG = Move.PROMOTION

            moves.append(move)
        
        # Capture
        for dir in captureDirection:
            targetSquare = startSquare + dir
            pieceOnTargetSquare = board.board[targetSquare]

            if pieceOnTargetSquare != None and not IsColor(pieceOnTargetSquare, color_to_move):
                move = Move(startSquare, targetSquare)
                move.CAPTURED_PIECE = pieceOnTargetSquare
                # Promotion
                if BoardRepresentation.RankIndex(targetSquare) == 7 or BoardRepresentation.RankIndex(targetSquare) == 0:
                    move.FLAG = Move.PROMOTION

                moves.append(move)


    def GenerateKnightMoves(self, moves, board, color_to_move, startSquare):
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

            startSquareColor = (BoardRepresentation.RankIndex(startSquare) + BoardRepresentation.FileIndex(startSquare)) % 2
            targetSquareColor = (BoardRepresentation.RankIndex(targetSquare) + BoardRepresentation.FileIndex(targetSquare)) % 2
            isSameColorSquare = startSquareColor == targetSquareColor

            if not isSameColorSquare and (pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move)):
                move = Move(startSquare, targetSquare)
                # Capture
                if pieceOnTargetSquare != None:
                    move.CAPTURED_PIECE = pieceOnTargetSquare
                
                moves.append(move)

    def GenerateKingMoves(self, moves, board, color_to_move, startSquare):
        for directionIndex in range(0, 8):
            targetSquare = startSquare + self.DIRECTION_OFFSETS[directionIndex]

            if targetSquare < 0 or targetSquare > 63:
                continue

            pieceOnTargetSquare = board.board[targetSquare]

            if pieceOnTargetSquare == None or not IsColor(pieceOnTargetSquare, color_to_move):
                move = Move(startSquare, targetSquare)
                # Capture
                if pieceOnTargetSquare != None:
                    move.CAPTURED_PIECE = pieceOnTargetSquare
                moves.append(move)

                # Castle kingside
                if (targetSquare == BoardRepresentation.f1 or targetSquare == BoardRepresentation.f8) and self.HasKingsideCastleRight(board, color_to_move):
                    castleKingSideSquare = targetSquare + 1
                    if board.board[castleKingSideSquare] == None:
                        castleMove = Move(startSquare, castleKingSideSquare)
                        castleMove.FLAG = Move.CASTLING
                        moves.append(castleMove)
                
                # Castle queenside
                if (targetSquare == BoardRepresentation.d1 or targetSquare == BoardRepresentation.d8) and self.HasQueensideCastleRight(board, color_to_move):
                    castleQueenSideSquare = targetSquare - 1
                    if board.board[castleQueenSideSquare] == None and board.board[castleQueenSideSquare-1] == None:
                        castleMove = Move(startSquare, castleQueenSideSquare)
                        castleMove.FLAG = Move.CASTLING
                        moves.append(castleMove)

        
    def GenerateSlidingMoves(self, moves, board, color_to_move, startSquare, piece):
        startDirIndex = 4 if IsBishop(piece) else 0
        endDirIndex = 4 if IsRook(piece) else 8

        for directionIndex in range(startDirIndex, endDirIndex):
            for n in range(self.NUM_SQUARES_TO_EDGE[startSquare][directionIndex]):
                targetSquare = startSquare + self.DIRECTION_OFFSETS[directionIndex] * (n+1)
                pieceOnTargetSquare = board[targetSquare]

                if pieceOnTargetSquare == None:
                    moves.append(Move(startSquare, targetSquare))
                    continue

                if IsColor(pieceOnTargetSquare, color_to_move):
                    break
                
                # Capture
                move = Move(startSquare, targetSquare)
                move.CAPTURED_PIECE = pieceOnTargetSquare
                moves.append(move)

                if not IsColor(pieceOnTargetSquare, color_to_move):
                    break

    def ComputeMoveData(self):
        for file in range(8):
            for rank in range(8):
                numNorth = 7 - rank
                numSouth = rank
                numWest = file
                numEast = 7 - file

                squareIndex = rank * 8 + file

                self.NUM_SQUARES_TO_EDGE[squareIndex] = [
                    numNorth,
                    numSouth,
                    numWest,
                    numEast,
                    min(numNorth, numWest),
                    min(numSouth, numEast),
                    min(numNorth, numEast),
                    min(numSouth, numWest)
                ]


    # Helper functions
    def HasKingsideCastleRight(self, board, color_to_move):
        CastleState = board.WhiteCastleState if color_to_move == WHITE else board.BlackCastleState
        return (CastleState & 0b01) == 0b01

    def HasQueensideCastleRight(self, board, color_to_move):
        CastleState = board.WhiteCastleState if color_to_move == WHITE else board.BlackCastleState
        return (CastleState & 0b10) == 0b10