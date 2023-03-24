import pygame
from pygame.locals import *
from frontend.Scene import Scene
import frontend.TitleScene as ts
import frontend.GameSceneHelper as gsh
import game.Players as pl

SQUARE_SIZE = 100
X_OFFSET_BOARD = 200
Y_OFFSET_BOARD = 200
X_OFFSET_CHECKERS = 250
Y_OFFSET_CHECKERS = 250

class GameScene(Scene):
	"""
	Page that contains the game. Initialised with game settings selected on the title screen.
	"""
	def __init__(self, one_player, red=None, difficulty=None):
		"""
		Initialise GameScene. If one player game, include other game and AI settings.
		params:
		  one_player: (bool) True if one player, False if two player, None if 0 player (AI vs AI)
		  red: (bool) True if player is red, false if AI is red
		  difficulty: (int) Level of difficulty of the AI opponent
		"""
		super().__init__()
		print(f"1p: {one_player}, red: {red}, diff: {difficulty}\n")
		# Fonts
		self.font = pygame.font.SysFont('Arial', 56)
		self.sfont = pygame.font.SysFont('Arial', 32)
		# Home Button
		self.home = self.font.render('Home', True, (255, 255, 255), (160,170,170))
		self.home_rect = self.home.get_rect(center=(100,50))
		# Game Status indicator text
		self.status_black_move = self.sfont.render('Black to move', True, (255, 255, 255))
		self.status_red_move = self.sfont.render('Red to move', True, (255, 255, 255))
		self.status_black_win = self.sfont.render('Black wins!', True, (255, 255, 255))
		self.status_red_win = self.sfont.render('Red wins!', True, (255, 255, 255))
		self.status_rect = self.status_black_move.get_rect(topleft=(200,150))
		# Board graphics
		self.board_rects = gsh.create_board_squares(SQUARE_SIZE, X_OFFSET_BOARD, Y_OFFSET_BOARD)
		# Game
		self.game = gsh.create_checker_game_from_selected_settings(one_player, red, difficulty)
		self.selected_square = None
		self.indicator_squares = None 
		self.active_colour = None
		# Count to be used to delay AI calculations: player move will be updated on screen first
		self.count = 0
		self.ai_generator = None


	def render(self, screen):
		screen.fill((0, 0, 0))
		screen.blit(self.home, self.home_rect)
		self.render_game_status_text(screen)
		gsh.render_board(screen, self.board_rects)
		gsh.render_checkers(screen, self.game.board, SQUARE_SIZE, X_OFFSET_CHECKERS, Y_OFFSET_CHECKERS)
		gsh.render_move_indicators(screen, self.indicator_squares, SQUARE_SIZE, X_OFFSET_CHECKERS, Y_OFFSET_CHECKERS)

	def render_game_status_text(self, screen):
		"""
		Render the status text based on the state of the game.
		Indicates who's move it is or who won.
		params:
		  screen: (Surface)
		"""
		if self.game.game_state == 0:
			if self.game.active_colour == -1:
				screen.blit(self.status_red_move, self.status_rect)
			elif self.game.active_colour == 1:
				screen.blit(self.status_black_move, self.status_rect)
		elif self.game.game_state == -1:
			screen.blit(self.status_red_win, self.status_rect)
		elif self.game.game_state == 1:
			screen.blit(self.status_black_win, self.status_rect)

	def update(self):
		if isinstance(self.game.active_player, pl.AI):
			if self.game.game_state == 0:
				if self.ai_generator == None:
					self.ai_generator = self.game.ai_move_generator()
				else:
					move = next(self.ai_generator)
					if move == None:
						self.ai_generator = None
					else:
						self.game.make_move(move[0], move[1])

	def handle_events(self, events):
		for e in events:
			if e.type == MOUSEBUTTONDOWN:
				home_pressed = True if self.home_rect.collidepoint(e.pos) else False
				if home_pressed:
					self.manager.go_to(ts.TitleScene())

				square_clicked = gsh.get_square_clicked(self.board_rects, e)
				if square_clicked != None:
					self.handle_square_click(square_clicked)

	def handle_square_click(self, square_clicked):
		"""
		Given a square has been clicked, handle the event.
		params:
		  square_clicked: (list : int) [row,col]
		"""
		if isinstance(self.game.active_player, pl.Human):
			if self.selected_square != None:
				if square_clicked in self.game.get_active_checker_squares():
					self.selected_square = square_clicked
					self.indicator_squares = self.game.get_move_indicator_squares(self.selected_square)
				else:
					self.game.make_move(self.selected_square, square_clicked)
					self.selected_square = None
					self.indicator_squares = None
			else:
				if square_clicked in self.game.get_active_checker_squares():
					self.selected_square = square_clicked
					self.indicator_squares = self.game.get_move_indicator_squares(self.selected_square)
				else:
					pass

						
						


