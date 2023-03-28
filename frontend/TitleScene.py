import pygame
from pygame.locals import *
from frontend.Scene import Scene
import frontend.GameScene as gs
import frontend.RulesScene as rs
import main as m

X_MID = m.WIN_WIDTH / 2
Y_MID = m.WIN_HEIGHT / 2

class TitleScene(Scene):
    """
    Page that greets the user. Contains buttons to select game options, start game, and check rules.
    """
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.SysFont('Arial', 56)
        self.title_font.set_underline(True)
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        # Game settings
        self.game_zero_player = False
        self.game_one_player = False
        self.game_two_player = False
        self.game_red = False
        self.game_black = False
        self.game_diff1 = False
        self.game_diff2 = False
        self.game_diff3 = False
        self.game_help = False
        self.game_regicide = False
        self.game_start_game = False
        # Text and Buttons
        # Title
        self.title = self.title_font.render('Aesthetically unappealing checkers.', True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(X_MID,50))
        # Rules button
        self.rules = self.font.render("Rules", True, (255,255,255), (160,170,170))
        self.rules_rect = self.rules.get_rect(center=(X_MID, 150))
        # Player count buttons
        self.zero_player = self.font.render("AI vs AI", True, (255,255,255), (160,170,170))
        self.zero_player_selected = self.font.render("AI vs AI", True, (255,255,255), (150,120,70))
        self.zero_player_rect = self.zero_player.get_rect(center=(X_MID + X_MID / 2, 550))
        self.one_player = self.font.render("One Player", True, (255,255,255), (160,170,170))
        self.one_player_selected = self.font.render("One Player", True, (255,255,255), (150,120,70))
        self.one_player_rect = self.one_player.get_rect(center=(X_MID - X_MID / 2, 300))
        self.two_player = self.font.render("Two Player", True, (255,255,255), (160,170,170))
        self.two_player_selected = self.font.render("Two Player", True, (255,255,255), (150,120,70))
        self.two_player_rect = self.two_player.get_rect(center=(X_MID + X_MID / 2, 300))
        # 1 Player option buttons
        self.play_as = self.font.render("Play as", True, (255,255,255))
        self.play_as_rect = self.play_as.get_rect(center=(X_MID - X_MID / 2, 380))
        self.red = self.font.render("Red", True, (255,255,255), (160,170,170))
        self.red_disabled = self.font.render("Red", True, (60,60,60), (90,90,90))
        self.red_selected = self.font.render("Red", True, (255,255,255), (150,120,70))
        self.red_rect = self.red.get_rect(center=(X_MID - 3 * X_MID / 4, 450))
        self.black = self.font.render("Black", True, (255,255,255), (160,170,170))
        self.black_disabled = self.font.render("Black", True, (60,60,60), (90,90,90))
        self.black_selected = self.font.render("Black", True, (255,255,255), (150,120,70))
        self.black_rect = self.black.get_rect(center=(X_MID - X_MID / 4, 450))
        self.difficulty_text = self.font.render("AI Difficulty", True, (255,255,255))
        self.difficulty_text_rect = self.difficulty_text.get_rect(center=(X_MID - X_MID / 2, 550))
        self.diff1 = self.font.render(" 1 ", True, (255,255,255), (160,170,170))
        self.diff1_disabled = self.font.render(" 1 ", True, (60,60,60), (90,90,90))
        self.diff1_selected = self.font.render(" 1 ", True, (255,255,255), (150,120,70))
        self.diff1_rect = self.diff1.get_rect(center=(X_MID - 3 * X_MID / 4, 650))
        self.diff2 = self.font.render(" 2 ", True, (255,255,255), (160,170,170))
        self.diff2_disabled = self.font.render(" 2 ", True, (60,60,60), (90,90,90))
        self.diff2_selected = self.font.render(" 2 ", True, (255,255,255), (150,120,70))
        self.diff2_rect = self.diff2.get_rect(center=(X_MID - X_MID / 2, 650))
        self.diff3 = self.font.render(" 3 ", True, (255,255,255), (160,170,170))
        self.diff3_disabled = self.font.render(" 3 ", True, (60,60,60), (90,90,90))
        self.diff3_selected = self.font.render(" 3 ", True, (255,255,255), (150,120,70))
        self.diff3_rect = self.diff3.get_rect(center=(X_MID - X_MID / 4, 650))
        # Additional Settings text
        self.additional = self.font.render("Additional Settings", True, (255,255,255))
        self.additional_rect = self.additional.get_rect(center=(X_MID, 750))
        # Help function button
        self.help = self.font.render("Help", True, (255,255,255), (160,170,170))
        self.help_selected = self.font.render("Help", True, (255,255,255), (150,120,70))
        self.help_rect = self.help.get_rect(center=(X_MID - X_MID / 4, 850))
        # Regicide Button
        self.regicide = self.font.render("Regicide", True, (255,255,255), (160,170,170))
        self.regicide_selected = self.font.render("Regicide", True, (255,255,255), (150,120,70))
        self.regicide_rect = self.regicide.get_rect(center=(X_MID + X_MID / 4, 850))
        # Start Game button
        self.start_game = self.font.render("Start Game", True, (255,255,255), (160,170,170))
        self.start_game_disabled = self.font.render("Start Game", True, (60,60,60), (90,90,90))
        self.start_game_rect = self.start_game.get_rect(center=(X_MID, 920))

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.rules, self.rules_rect)
        screen.blit(self.play_as, self.play_as_rect)
        screen.blit(self.difficulty_text, self.difficulty_text_rect)
        screen.blit(self.additional, self.additional_rect)
        if self.game_help:
            screen.blit(self.help_selected, self.help_rect)
        else:
            screen.blit(self.help, self.help_rect)

        if self.game_regicide:
            screen.blit(self.regicide_selected, self.regicide_rect)
        else:
            screen.blit(self.regicide, self.regicide_rect)

        if self.game_zero_player:
            screen.blit(self.zero_player_selected, self.zero_player_rect)
        else:
            screen.blit(self.zero_player, self.zero_player_rect)
            

        if not self.game_one_player and not self.game_two_player:
            screen.blit(self.one_player, self.one_player_rect)
            screen.blit(self.two_player, self.two_player_rect)
            screen.blit(self.red_disabled, self.red_rect)
            screen.blit(self.black_disabled, self.black_rect)
            screen.blit(self.diff1_disabled, self.diff1_rect)
            screen.blit(self.diff2_disabled, self.diff2_rect)
            screen.blit(self.diff3_disabled, self.diff3_rect)
            if self.game_zero_player:
                screen.blit(self.start_game, self.start_game_rect)
            else:
                screen.blit(self.start_game_disabled, self.start_game_rect)
        elif self.game_two_player:
            screen.blit(self.one_player, self.one_player_rect)
            screen.blit(self.two_player_selected, self.two_player_rect)
            screen.blit(self.red_disabled, self.red_rect)
            screen.blit(self.black_disabled, self.black_rect)
            screen.blit(self.diff1_disabled, self.diff1_rect)
            screen.blit(self.diff2_disabled, self.diff2_rect)
            screen.blit(self.diff3_disabled, self.diff3_rect)
            screen.blit(self.start_game, self.start_game_rect)
        elif self.game_one_player:
            screen.blit(self.one_player_selected, self.one_player_rect)
            screen.blit(self.two_player, self.two_player_rect)
            if not self.game_red and not self.game_black:
                screen.blit(self.red, self.red_rect)
                screen.blit(self.black, self.black_rect)
                screen.blit(self.diff1_disabled, self.diff1_rect)
                screen.blit(self.diff2_disabled, self.diff2_rect)
                screen.blit(self.diff3_disabled, self.diff3_rect)
                screen.blit(self.start_game_disabled, self.start_game_rect)
            elif self.game_red:
                screen.blit(self.red_selected, self.red_rect)
                screen.blit(self.black, self.black_rect)
                if not self.game_diff1 and not self.game_diff2 and not self.game_diff3:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game_disabled, self.start_game_rect)
                elif self.game_diff1:
                    screen.blit(self.diff1_selected, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)
                elif self.game_diff2:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2_selected, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)
                elif self.game_diff3:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3_selected, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)
            elif self.game_black:
                screen.blit(self.red, self.red_rect)
                screen.blit(self.black_selected, self.black_rect)
                if not self.game_diff1 and not self.game_diff2 and not self.game_diff3:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game_disabled, self.start_game_rect)
                elif self.game_diff1:
                    screen.blit(self.diff1_selected, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)
                elif self.game_diff2:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2_selected, self.diff2_rect)
                    screen.blit(self.diff3, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)
                elif self.game_diff3:
                    screen.blit(self.diff1, self.diff1_rect)
                    screen.blit(self.diff2, self.diff2_rect)
                    screen.blit(self.diff3_selected, self.diff3_rect)
                    screen.blit(self.start_game, self.start_game_rect)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                rules_pressed = True if self.rules_rect.collidepoint(e.pos) else False
                if rules_pressed:
                    self.manager.go_to(rs.RulesScene())
                
                help_pressed = True if self.help_rect.collidepoint(e.pos) else False
                if help_pressed:
                    self.game_help = True if not self.game_help else False

                regicide_pressed = True if self.regicide_rect.collidepoint(e.pos) else False
                if regicide_pressed:
                    self.game_regicide = True if not self.game_regicide else False

                zero_player_pressed = True if self.zero_player_rect.collidepoint(e.pos) else False
                if zero_player_pressed:
                    self.game_zero_player = True
                    self.game_one_player = False
                    self.game_two_player = False
                    self.game_start_game = True

                one_player_pressed = True if self.one_player_rect.collidepoint(e.pos) else False
                if one_player_pressed:
                    self.game_zero_player = False
                    self.game_one_player = True
                    self.game_two_player = False
                    self.game_start_game = False
                
                two_player_pressed = True if self.two_player_rect.collidepoint(e.pos) else False
                if two_player_pressed:
                    self.game_zero_player = False
                    self.game_one_player = None
                    self.game_one_player = False
                    self.game_two_player = True
                    self.game_red = False
                    self.game_black = False
                    self.game_diff1 = False
                    self.game_diff2 = False
                    self.game_diff3 = False
                    self.game_start_game = True
                
                red_pressed = True if self.red_rect.collidepoint(e.pos) else False
                if red_pressed and self.game_one_player:
                    self.game_red = True
                    self.game_black = False

                black_pressed = True if self.black_rect.collidepoint(e.pos) else False
                if black_pressed and self.game_one_player:
                    self.game_red = False
                    self.game_black = True

                diff1_pressed = True if self.diff1_rect.collidepoint(e.pos) else False
                if diff1_pressed and self.game_one_player:
                    if self.game_red or self.game_black:
                        self.game_diff1 = True
                        self.game_diff2 = False
                        self.game_diff3 = False
                        self.game_start_game = True

                diff2_pressed = True if self.diff2_rect.collidepoint(e.pos) else False
                if diff2_pressed and self.game_one_player:
                    if self.game_red or self.game_black:
                        self.game_diff1 = False
                        self.game_diff2 = True
                        self.game_diff3 = False
                        self.game_start_game = True
                
                diff3_pressed = True if self.diff3_rect.collidepoint(e.pos) else False
                if diff3_pressed and self.game_one_player:
                    if self.game_red or self.game_black:
                        self.game_diff1 = False
                        self.game_diff2 = False
                        self.game_diff3 = True
                        self.game_start_game = True

                start_game_pressed = True if self.start_game_rect.collidepoint(e.pos) else False
                if start_game_pressed and self.game_start_game:
                    if self.game_zero_player:
                        # AI vs AI game
                        self.manager.go_to(gs.GameScene(None, regicide=self.game_regicide))
                    elif self.game_one_player:
                        difficulty = 0
                        if self.game_diff1 == True:
                            difficulty = 1
                        elif self.game_diff2 == True:
                            difficulty = 2
                        else:
                            difficulty = 3
                        self.manager.go_to(gs.GameScene(self.game_one_player, self.game_red, difficulty, self.game_help, regicide=self.game_regicide))
                    else:
                        self.manager.go_to(gs.GameScene(self.game_one_player, help=self.game_help, regicide=self.game_regicide))
