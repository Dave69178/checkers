import pygame
import game.Checkers as c
import game.Players as pl

"""
Helper functions for GameScene.
"""

def create_board_squares(square_size, x_offset, y_offset):
	"""
	Create rects for each square in the board
	params:
		square_size: (int) size of each square on the board
		x_offset: (int) distance from left side of screen
		y_offset: (int) distance from top of screen
	return: (2D list of pygame.Rects)
	"""
	board = [[0 for col in range(8)] for row in range(8)]
	for row in range(8):
		y_pos = y_offset + row * square_size
		for col in range(8):
			x_pos = x_offset + col * square_size
			board[row][col] = pygame.Rect((x_pos, y_pos), (square_size, square_size))
	return board

def render_board(screen, board_rects):
	"""
	To be called in the scene's render function to render the board.
	params:
		screen: (Surface) The Surface to draw to
		board_rects: (2D array of pygame.Rect's) Squares to draw
	"""
	for row in range(8):
		for col in range(8):
			if row % 2 == 0:
				if col % 2 == 0:
					pygame.draw.rect(screen, (255,255,255), board_rects[row][col])
				else:
					pygame.draw.rect(screen, (145,110,70), board_rects[row][col])
			else:
				if col % 2 == 0:
					pygame.draw.rect(screen, (145,110,70), board_rects[row][col])
				else:
					pygame.draw.rect(screen, (255,255,255), board_rects[row][col])

def render_checkers(screen, board, square_size, x_offset, y_offset):
	"""
	Draws checkers on the board. To be called in the scene's render function after render_board.
	params:
		screen: (Surface) The Surface to draw to
		board: (2D list, ints representing element in each square) The game's board
		square_size: (int) size of each square on the board
		x_offset: (int) distance from left side of screen
		y_offset: (int) distance from top of screen
	"""
	for row in range(8):
		y_pos = y_offset + row * square_size
		for col in range(8):
			x_pos = x_offset + col * square_size
			if board[row][col] == 0:
				continue
			elif board[row][col] == 1:
				pygame.draw.circle(screen, (0,0,0), (x_pos, y_pos), square_size * 2/5)
			elif board[row][col] == 2:
				pygame.draw.rect(screen, (0,0,0), pygame.Rect((x_pos - square_size * 2/5, y_pos - square_size * 2/5), (square_size * 4/5, square_size * 4/5)))
			elif board[row][col] == -1:
				pygame.draw.circle(screen, (255,0,0), (x_pos, y_pos), square_size * 2/5)
			elif board[row][col] == -2:
				pygame.draw.rect(screen, (255,0,0), pygame.Rect((x_pos - square_size * 2/5, y_pos - square_size * 2/5), (square_size * 4/5, square_size * 4/5)))

def render_move_indicators(screen, indicator_squares, square_size, x_offset, y_offset):
	"""
	Draws move indicators to the board. To be called after render_board in the scene's render function.
	params:
		screen: (Surface) The Surface to draw to
		indicator_squares: (list of [row,col] elements) The squares that should be highlighted according to selection and game state.
		square_size: (int) size of each square on the board
		x_offset: (int) distance from left side of screen
		y_offset: (int) distance from top of screen
	"""
	if indicator_squares == None:
		return
	for ind in indicator_squares:
		x_pos = x_offset + ind[1] * square_size
		y_pos = y_offset + ind[0] * square_size
		pygame.draw.circle(screen, (110, 165, 200), (x_pos, y_pos), square_size * 1/6)

def get_square_clicked(square_rects, event):
	"""
	If a square is clicked, return the index of that square, otherwise None.
	params:
	  square_rects: (2D list of pygame.Rect's) Rects of the squares making up the board
	  event: (pygame event)
	return: [int, int] ([row, col] if square), else None
	"""
	for row in range(8):
		for col in range(8):
			if square_rects[row][col].collidepoint(event.pos):
				return [row, col]
	return None

def create_checker_game_from_selected_settings(one_player, red, difficulty):
	"""
	Create players and game based on settings selected on title screen.
	params:
	  one_player: (bool) True if one player, False if Two
	  red: (bool) True if player is red, False if black (None if two player game)
	  difficulty: (int) in range:[1,2,3], None if two player game
	return: (Checkers) Game object
	"""
	if one_player == None:
		print("AI vs AI")
		red_player = pl.AI(-1, 2)
		black_player = pl.AI(1, 3)
		return c.Checkers(red_player, black_player)
	if one_player:
		print("one player")
		if red:
			red_player = pl.Human(-1)
			black_player = pl.AI(1, difficulty)
		else:
			red_player = pl.AI(-1, difficulty)
			black_player = pl.Human(1)
	else:
		print("two player")
		red_player = pl.Human(-1)
		black_player = pl.Human(1)
	return c.Checkers(red_player, black_player)