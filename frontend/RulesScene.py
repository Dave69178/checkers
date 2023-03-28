import pygame
from pygame.locals import *
from frontend.Scene import Scene
import frontend.TitleScene as ts
import main as m

SETUP_TEXT = '- The game is played on an 8 by 8 board - where checkers can move on dark squares only.\n- Each player starts with 12 checkers arranged on the 3 rows nearest to them\n- One player is a light colour, the other a dark colour checker.\n- The dark checkered player is first to move. Players then alternate taking moves.'
MOVEMENT_TEXT = '- Checkers can be moved one square diagonally forward to an empty square\n- A checker can capture an opponent piece by "jumping" over it diagonally forward\n- Multiple "jumps" can be taken in a single turn\n- If a capture is available, the player must perform a capture\n- If a checker reaches the opposite side of the board it is crowned a King\n- Crowning causes the player\'s turn to end\n- A King can move and capture backwards as well as forwards'
END_CONDITION_TEXT = '- A player wins the game if they capture all of their opponent\'s checkers\n- They may also win if their opponent has no legal moves'
ADDITIONAL_TEXT = '- Regicide enables a condition where capturing a King crowns the checker that captured it\n- If this happens the turn ends immediately'
PARAGRAPH_FONT_SIZE = int((30/1200) * m.WIN_HEIGHT)
X_MID = m.WIN_WIDTH / 2
Y_MID = m.WIN_WIDTH / 2

class RulesScene(Scene):
    """
    Page that explains the rules of checkers.
    """
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', PARAGRAPH_FONT_SIZE)
        # Title
        self.title = self.font.render('Rules of Checkers', True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(X_MID,(50/1200) * m.WIN_HEIGHT))
        # Home Button
        self.home = self.font.render('Home', True, (255, 255, 255), (160,170,170))
        self.home_rect = self.home.get_rect(center=((100/1200)*m.WIN_WIDTH,(50/1200) * m.WIN_HEIGHT))
        # Game setup
        self.setup_title = self.font.render('Game Setup', True, (255, 255, 255))
        self.setup_title_rect = self.setup_title.get_rect(center=(X_MID,(150/1200) * m.WIN_HEIGHT))
        # Movement
        self.movement_title = self.font.render('Movement', True, (255, 255, 255))
        self.movement_title_rect = self.movement_title.get_rect(center=(X_MID,(400/1200) * m.WIN_HEIGHT))
        # End conditions
        self.end_condition_title = self.font.render('End Conditions', True, (255, 255, 255))
        self.end_condition_title_rect = self.end_condition_title.get_rect(center=(X_MID,(770/1200) * m.WIN_HEIGHT))
        # Additional
        self.additional_title = self.font.render('Additional Info', True, (255, 255, 255))
        self.additional_title_rect = self.additional_title.get_rect(center=(X_MID,(940/1200) * m.WIN_HEIGHT))

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.home, self.home_rect)
        screen.blit(self.setup_title, self.setup_title_rect)
        render_multi_line(screen, self.sfont, (255,255,255), SETUP_TEXT, 20, (200/1200) * m.WIN_HEIGHT, PARAGRAPH_FONT_SIZE + 2)
        screen.blit(self.movement_title, self.movement_title_rect)
        render_multi_line(screen, self.sfont, (255,255,255), MOVEMENT_TEXT, 20, (450/1200) * m.WIN_HEIGHT, PARAGRAPH_FONT_SIZE + 2)
        screen.blit(self.end_condition_title, self.end_condition_title_rect)
        render_multi_line(screen, self.sfont, (255,255,255), END_CONDITION_TEXT, 20, (820/1200) * m.WIN_HEIGHT, PARAGRAPH_FONT_SIZE + 2)
        screen.blit(self.additional_title, self.additional_title_rect)
        render_multi_line(screen, self.sfont, (255,255,255), ADDITIONAL_TEXT, 20, (980/1200) * m.WIN_HEIGHT, PARAGRAPH_FONT_SIZE + 2)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                home_pressed = True if self.home_rect.collidepoint(e.pos) else False
                if home_pressed:
                    self.manager.go_to(ts.TitleScene())

def render_multi_line(screen, font, colour, text, x, y, fsize):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(font.render(l, 0, colour), (x, y + fsize*i))