import time
import game.CheckersHelper as ch
import ai.Search as s
import ai.HelpSystem as help
import game.Players as pl

class Checkers:
	def __init__(self, red_player, black_player, board=None, active_colour=None, help=False, regicide=False) -> None:
		"""
		Initialise Checkers game.
		params:
		  red_player: (Player)
		  black_player: (Player)
		  board (optional): (list[list : int]) Provide a different starting position
		  active_colour (optional): int
		  help (optional): (bool)
		  regicide (optional): (bool)
		"""
		if board == None:
			self.board = ch.create_starting_board()
			self.active_colour = 1
			self.active_player = black_player
		else:
			self.board = board
			if active_colour == None:
				raise Exception("No active colour provided.")
			else:
				self.active_colour = active_colour
				self.active_player = red_player if active_colour == -1 else black_player
		self.red_player = red_player
		self.black_player = black_player
		self.turn_count = 0
		self.game_state = 0
		self.legal_moves = ch.get_all_one_step_moves_for_colour(self.board, self.active_colour)
		self.game_log = []
		self.help = help
		self.regicide = regicide

	def make_move(self, start_square, end_square):
		"""
		Given a move, check whether it is legal or not. If it is, make move. Check end turn conditions
		params:
		  start_square: ([int, int]) row,col
		  end_square: ([int,int]) row,col
		"""
		is_legal_move = ch.is_move_legal(self.board, self.legal_moves, self.active_colour, start_square, end_square)
		if is_legal_move:
			colour = "Black" if self.active_colour == 1 else "Red"
			ch.log_message(self.game_log, f"{colour} made move: {start_square} to {end_square}")
			if ch.update_board(self.board, start_square, end_square, self.regicide):
				self._end_turn()
			else:
				self.legal_moves = ch.get_all_one_step_moves_for_colour(self.board, self.active_colour)
		else:
			ch.log_message(self.game_log, "That is not a legal move.")

	def ai_move_generator(self):
		"""
		Generator that returns a step of the move sequence upon each call.
		yield: (list : [row,col]) - [[row,col], [row,col]]. Yields None to indicate end of moves
		"""
		start = time.perf_counter()
		ai_sequence = s.get_ai_move_multiprocess(self.board, self.active_colour, self.active_player.depth, self.active_player.heuristic_function, self.regicide)
		end = time.perf_counter()
		steps = len(ai_sequence)
		move = 0
		if end - start < 1:
			time.sleep(1)
			yield ai_sequence[0]
			move += 1
		else:
			yield ai_sequence[0]
			move += 1
		while move < steps:
			time.sleep(1)
			yield ai_sequence[move]
			move += 1
		yield None

	def _end_turn(self):
		"""
		Checks to be done at end of turn. Swap sides, check for win etc.      
		"""
		end_condition = ch.check_end_conditions(self.board, self.active_colour)
		if end_condition == 0:
			self.turn_count += 1
			self.active_colour = 1 if self.active_colour == -1 else -1
			self.active_player = self.red_player if self.active_colour == -1 else self.black_player
			self.legal_moves = ch.get_all_one_step_moves_for_colour(self.board, self.active_colour)
			if self.help and isinstance(self.active_player, pl.Human):
				help.get_help_message_for_position(self)
		else:
			self.game_state = end_condition
			self.turn_count += 1
			self.active_colour = 1 if self.active_colour == -1 else -1
			self.active_player = self.red_player if self.active_colour == -1 else self.black_player
			self.legal_moves = ch.get_all_one_step_moves_for_colour(self.board, self.active_colour)
			
	def get_active_checker_squares(self):
		"""
		For the active player, return the squares of their checkers
		return: (list[list : [row,col]])
		"""
		active_squares = []
		for row in range(8):
			for col in range(8):
				if self.board[row][col] * self.active_colour > 0:
					active_squares.append([row,col])
		return active_squares
	
	def get_move_indicator_squares(self, selected_square):
		"""
		Get the legal moves for a given square.
		params:
		  selected_square: (list : int) [row,col]
		"""
		return self.legal_moves[selected_square[0]][selected_square[1]]

