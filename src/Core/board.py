import pygame

from Core.const import *
from Core.pieces import *
from Core.moves import *

class Board:
    def __init__(self):
        self.board = [None]*64
        self.pieces = load_pieces()
        self.LoadPositionFromFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

        # Mouse
        self.grabbed = False
        self.grabbed_piece = None

        # Move
        self.moved = False
        self.moved_old = None
        self.moved_new = None
        self.moved_indices = [None, None]

        # Logic
        self.color_to_move = WHITE
        self.currentPieceMoves = []

        ComputeMoveData()
        GenerateMoves(self.board, self.color_to_move)
    
    

    def MakeMove(self, file, rank):
        self.board[rank * 8 + file] = self.grabbed_piece

        self.grabbed = False
        self.grabbed_piece = None
        
        self.moved_new = rank * 8 + file

        if self.moved_new != self.moved_old:
            self.moved = True
            self.moved_indices[0] = self.moved_old
            self.moved_indices[1] = self.moved_new

            self.color_to_move = WHITE if self.color_to_move == BLACK else BLACK
            GenerateMoves(self.board, self.color_to_move)
        
        self.currentPieceMoves = []

    def MouseDrag(self):
        if self.grabbed and not pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            file = int(mouse_x/(BOARD_WIDTH/8))
            rank = 7 - int(mouse_y/(BOARD_HEIGHT/8))
            
            self.MakeMove(file, rank)

        elif pygame.mouse.get_pressed()[0] and not self.grabbed:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            file = int(mouse_x/(BOARD_WIDTH/8))
            rank = 7 - int(mouse_y/(BOARD_HEIGHT/8))
            piece = self.board[rank * 8 + file]

            if piece != None and IsColor(piece, self.color_to_move):
                self.grabbed = True
                self.grabbed_piece = piece

                self.board[rank * 8 + file] = None

                self.moved_new = None
                self.moved_old = rank * 8 + file

                # Create legal moves for current piece
                for move in legalMoves:
                    if (rank*8+file) == move.START_SQUARE:
                        self.currentPieceMoves.append(move.TARGET_SQUARE)


    def LoadPositionFromFen(self, fen):
        pieceTypeFromSymbol = {
            'k' : KING,
            'p' : PAWN,
            'n' : KNIGHT,
            'b' : BISHOP,
            'r' : ROOK,
            'q' : QUEEN
        }

        file = 0
        rank = 7

        for symbol in fen:
            if symbol == "/":
                file = 0
                rank -= 1
            else:
                if symbol.isnumeric():
                    file += int(symbol)
                else:
                    pieceColor = WHITE if symbol.isupper() else BLACK
                    pieceType = pieceTypeFromSymbol[symbol.lower()]
                    self.board[rank * 8 + file] = pieceColor | pieceType
                    file += 1

    def draw(self, window):
        # Board
        for i, square in enumerate(self.board):
            x = i % 8
            y = 7 - (i - x) / 8

            color = WHITE_COLOR if (x+y) % 2 == 0 else BLACK_COLOR

            rect = pygame.Rect(x*BOARD_WIDTH/8, y*BOARD_HEIGHT/8, BOARD_WIDTH/8, BOARD_HEIGHT/8)
            pygame.draw.rect(window, color, rect)

            # Move colors
            if self.moved:
                if i in self.moved_indices:
                    move_color = MOVE_COLOR_OLD if i == self.moved_indices[0] else MOVE_COLOR_NEW
                    pygame.draw.rect(window, move_color, rect)

            # Legal moves
            if i in self.currentPieceMoves:
                legal_color = LEGAL_MOVE_COLOR_WHITE if (x+y) % 2 == 0 else LEGAL_MOVE_COLOR_BLACK
                pygame.draw.rect(window, legal_color, rect)

            if square != None:
                img = pygame.transform.scale(self.pieces[square], (BOARD_WIDTH/8, BOARD_HEIGHT/8))

                window.blit(img, (x*BOARD_WIDTH/8, y*BOARD_HEIGHT/8))
        
        # Mouse grabbed piece
        if self.grabbed:
            img = pygame.transform.scale(self.pieces[self.grabbed_piece], (BOARD_WIDTH/8, BOARD_HEIGHT/8))
            mouse_pos = pygame.mouse.get_pos()

            window.blit(img, (mouse_pos[0]-img.get_width()/2, mouse_pos[1]-img.get_height()/2))