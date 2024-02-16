import pygame
from os import chdir

NONE = 0
KING = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6

WHITE = 8
BLACK = 16

TYPEMASK = 0b00111
BLACKMASK = 0b10000
WHITEMASK = 0b01000
COLORMASK = WHITEMASK | BLACKMASK


def IsColor(piece, color):
    return (piece & COLORMASK) == color

def IsSlidingPiece(piece):
    return (piece & 0b100) != 0

def IsKing(piece):
    return (piece & TYPEMASK) == 1

def IsBishop(piece):
    return (piece & TYPEMASK) == 4

def IsRook(piece):
    return (piece & TYPEMASK) == 5

def IsKnight(piece):
    return (piece & TYPEMASK) == 3


def load_pieces():
    chdir("..")

    pieces = {}

    pieces[WHITE | KING] = pygame.image.load(f"assets\\{WHITE}_{KING}.png").convert_alpha()
    pieces[WHITE | QUEEN] = pygame.image.load(f"assets\\{WHITE}_{QUEEN}.png").convert_alpha()
    pieces[WHITE | BISHOP] = pygame.image.load(f"assets\\{WHITE}_{BISHOP}.png").convert_alpha()
    pieces[WHITE | KNIGHT] = pygame.image.load(f"assets\\{WHITE}_{KNIGHT}.png").convert_alpha()
    pieces[WHITE | ROOK] = pygame.image.load(f"assets\\{WHITE}_{ROOK}.png").convert_alpha()
    pieces[WHITE | PAWN] = pygame.image.load(f"assets\\{WHITE}_{PAWN}.png").convert_alpha()

    pieces[BLACK | KING] = pygame.image.load(f"assets\\{BLACK}_{KING}.png").convert_alpha()
    pieces[BLACK | QUEEN] = pygame.image.load(f"assets\\{BLACK}_{QUEEN}.png").convert_alpha()
    pieces[BLACK | BISHOP] = pygame.image.load(f"assets\\{BLACK}_{BISHOP}.png").convert_alpha()
    pieces[BLACK | KNIGHT] = pygame.image.load(f"assets\\{BLACK}_{KNIGHT}.png").convert_alpha()
    pieces[BLACK | ROOK] = pygame.image.load(f"assets\\{BLACK}_{ROOK}.png").convert_alpha()
    pieces[BLACK | PAWN] = pygame.image.load(f"assets\\{BLACK}_{PAWN}.png").convert_alpha()

    return pieces