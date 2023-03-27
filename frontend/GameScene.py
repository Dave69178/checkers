import pygame
import datetime as dt
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
	def __init__(self, one_player, red=None, difficulty=None, help=False, regicide=False):
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
		self.logfont = pygame.font.SysFont('Arial', 25)
		# Home Button
		self.home = self.font.render('Home', True, (255, 255, 255), (160,170,170))
		self.home_rect = self.home.get_rect(center=(100,50))
		# Game Status indicator text
		self.status_black_move = self.sfont.render('Black to move', True, (255, 255, 255))
		self.status_red_move = self.sfont.render('Red to move', True, (255, 255, 255))
		self.status_black_win = self.sfont.render('Black wins!', True, (255, 255, 255))
		self.status_red_win = self.sfont.render('Red wins!', True, (255, 255, 255))
		self.status_rect = self.status_black_move.get_rect(center=(600,90))
		# Index numbers
		# Rows
		self.row0 = self.sfont.render('0', True, (255, 255, 255))
		self.row0_rect = self.row0.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50))
		self.row1 = self.sfont.render('1', True, (255, 255, 255))
		self.row1_rect = self.row1.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE))
		self.row2 = self.sfont.render('2', True, (255, 255, 255))
		self.row2_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 2))
		self.row3 = self.sfont.render('3', True, (255, 255, 255))
		self.row3_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 3))
		self.row4 = self.sfont.render('4', True, (255, 255, 255))
		self.row4_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 4))
		self.row5 = self.sfont.render('5', True, (255, 255, 255))
		self.row5_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 5))
		self.row6 = self.sfont.render('6', True, (255, 255, 255))
		self.row6_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 6))
		self.row7 = self.sfont.render('7', True, (255, 255, 255))
		self.row7_rect = self.row2.get_rect(center=(X_OFFSET_BOARD - 50, Y_OFFSET_BOARD + 50 + SQUARE_SIZE * 7))
		# Columns
		self.col0 = self.sfont.render('0', True, (255, 255, 255))
		self.col0_rect = self.col0.get_rect(center=(X_OFFSET_BOARD + 50, Y_OFFSET_BOARD - 50))
		self.col1 = self.sfont.render('1', True, (255, 255, 255))
		self.col1_rect = self.col1.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE, Y_OFFSET_BOARD - 50))
		self.col2 = self.sfont.render('2', True, (255, 255, 255))
		self.col2_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50  + SQUARE_SIZE * 2, Y_OFFSET_BOARD - 50))
		self.col3 = self.sfont.render('3', True, (255, 255, 255))
		self.col3_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE * 3, Y_OFFSET_BOARD - 50))
		self.col4 = self.sfont.render('4', True, (255, 255, 255))
		self.col4_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE * 4, Y_OFFSET_BOARD - 50))
		self.col5 = self.sfont.render('5', True, (255, 255, 255))
		self.col5_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE * 5, Y_OFFSET_BOARD - 50))
		self.col6 = self.sfont.render('6', True, (255, 255, 255))
		self.col6_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE * 6, Y_OFFSET_BOARD - 50))
		self.col7 = self.sfont.render('7', True, (255, 255, 255))
		self.col7_rect = self.col2.get_rect(center=(X_OFFSET_BOARD + 50 + SQUARE_SIZE * 7, Y_OFFSET_BOARD - 50))
		# Board graphics
		self.board_rects = gsh.create_board_squares(SQUARE_SIZE, X_OFFSET_BOARD, Y_OFFSET_BOARD)
		# Message log
		self.message_log = []
		self.log_surface = pygame.Surface((SQUARE_SIZE * 8, 150))
		self.log_surface.fill((255,255,255))
		self.log_surface_rect = self.log_surface.get_rect(center=(600,1100))
		# Game
		self.game = gsh.create_checker_game_from_selected_settings(one_player, red, difficulty, help, regicide)
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
		screen.blit(self.row0, self.row0_rect)
		screen.blit(self.row1, self.row1_rect)
		screen.blit(self.row2, self.row2_rect)
		screen.blit(self.row3, self.row3_rect)
		screen.blit(self.row4, self.row4_rect)
		screen.blit(self.row5, self.row5_rect)
		screen.blit(self.row6, self.row6_rect)
		screen.blit(self.row7, self.row7_rect)
		screen.blit(self.col0, self.col0_rect)
		screen.blit(self.col1, self.col1_rect)
		screen.blit(self.col2, self.col2_rect)
		screen.blit(self.col3, self.col3_rect)
		screen.blit(self.col4, self.col4_rect)
		screen.blit(self.col5, self.col5_rect)
		screen.blit(self.col6, self.col6_rect)
		screen.blit(self.col7, self.col7_rect)
		gsh.render_board(screen, self.board_rects)
		gsh.render_checkers(screen, self.game.board, SQUARE_SIZE, X_OFFSET_CHECKERS, Y_OFFSET_CHECKERS)
		gsh.render_move_indicators(screen, self.indicator_squares, SQUARE_SIZE, X_OFFSET_CHECKERS, Y_OFFSET_CHECKERS)
		self.render_log(screen, self.log_surface)

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
		self.update_log()
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

	def render_log(self, screen, log_surface):
		"""
		Given a log Surface object, render it to the screen.
		params:
		  screen: (Surface)
		  log_surface: (Surface)
		"""
		screen.blit(log_surface, self.log_surface_rect)
	
	def update_log(self):
		self.log_surface = pygame.Surface((SQUARE_SIZE * 8, 150))
		self.log_surface.fill((255,255,255))
		self.message_log = self.game.game_log
		y_pos = 0
		num_messages = 4
		if len(self.message_log) < 4:
			num_messages = len(self.message_log)
		for message in self.message_log[-num_messages:]:
			message_text = self.logfont.render(message, False, (0, 0, 0))
			self.log_surface.blit(message_text, (0, y_pos))
			y_pos += 34
						
						


