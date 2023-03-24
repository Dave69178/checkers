import pygame
from pygame.locals import *
from frontend.SceneManager import SceneMananger

WIN_WIDTH = 1200
WIN_HEIGHT = 1200

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 0
FLAGS = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, DEPTH, FLAGS)
    pygame.display.set_caption("Checkers")
    timer = pygame.time.Clock()
    running = True

    manager = SceneMananger()

    while running:
        timer.tick(60)

        if pygame.event.get(QUIT):
            running = False
            return
        
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
    
    return 0

if __name__=="__main__":
    main()