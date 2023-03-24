import pygame
from pygame.locals import *
from frontend.Scene import Scene
import frontend.TitleScene as ts

class RulesScene(Scene):
    """
    Page that explains the rules of checkers.
    """
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        # Title
        self.title = self.font.render('Rules', True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(600,50))
        # Home Button
        self.home = self.font.render('Home', True, (255, 255, 255), (160,170,170))
        self.home_rect = self.home.get_rect(center=(100,50))

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.home, self.home_rect)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                home_pressed = True if self.home_rect.collidepoint(e.pos) else False
                if home_pressed:
                    self.manager.go_to(ts.TitleScene())