import pygame, sys

from Core.board import Board

pygame.init()
pygame.display.set_caption("Chess")

def main():
    WIDTH, HEIGHT = 600, 600
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    board = Board()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        board.MouseDrag()

        screen.fill((0, 0, 0))
        board.draw(screen)
        
        pygame.display.update()

if __name__ == "__main__":
    main()