import pygame, sys

from board.const import *
from board.board import Board

pygame.init()
pygame.display.set_caption("Chess")

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    board = Board()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        board.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()