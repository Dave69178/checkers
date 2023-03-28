import copy
import numpy as np
import multiprocessing
import math
import game.CheckersHelper as ch

class Node:
	def __init__(self, board, active_colour, visited, parent) -> None:
		"""
		params:
		  board:
		  active_colour: player who's turn it is (other player made move that ended in position)
		  visited:
		  parent:
		"""
		self.board = board
		self.active_colour = active_colour
		self.visited = visited
		self.parent = parent


def alpha_beta(node : Node, depth, alpha, beta, maximising_player, heuristic_function, ai_colour, regicide):
	"""
	Implement minimax with alpha beta pruning.
	params:
	  node: (Node)
	  depth: (int)
	  alpha: (int)
	  beta: (int)
	  maximising_player: (bool)
	return: (int) value
	"""
	last_move_colour = 1 if node.active_colour == -1 else -1
	end_condition = ch.check_end_conditions(node.board, last_move_colour)
	if depth == 0 or end_condition != 0:
		if end_condition != 0:
			# Return positive inf if ai wins, negative infinity if opponent wins
			return ai_colour * end_condition * math.inf
		else:
			return heuristic_function(node.board, ai_colour)
	if maximising_player:
		value = -math.inf
		for child_board in ch.get_all_turn_end_positions(node.board, node.active_colour, regicide):
			child_active_colour = 1 if node.active_colour == -1 else -1
			child_node = Node(child_board, child_active_colour, False, node)
			value = max(value, alpha_beta(child_node, depth - 1, alpha, beta, False, heuristic_function, ai_colour, regicide))
			if value > beta:
				break
			alpha = max(alpha, value)
		return value
	else:
		value = math.inf
		for child_board in ch.get_all_turn_end_positions(node.board, node.active_colour, regicide):
			child_active_colour = 1 if node.active_colour == -1 else -1
			child_node = Node(child_board, child_active_colour, False, node)
			value = min(value, alpha_beta(child_node, depth - 1, alpha, beta, True, heuristic_function, ai_colour, regicide))
			if value < alpha:
				break
			beta = min(beta, value)
		return value


def get_ai_move(board, ai_colour, depth, heuristic_function, regicide):
	"""
	For the position, find best move by applying minimax w/ alpha-beta pruning.
	params:
	  board: (list[list : int])
	  ai_colour: (int)
	  depth: (int)
	  heuristic_function: (function(board, ai_colour))
	"""
	active_colour_after_move = 1 if ai_colour == -1 else -1
	sequences = ch.get_all_move_sequences(board, ai_colour, regicide)
	values = []
	for seq in sequences:
		temp_board = copy.deepcopy(board)
		for move in seq:
			ch.update_board(temp_board, move[0], move[1], regicide)
		position_node = Node(temp_board, active_colour_after_move, True, None)
		values.append(alpha_beta(position_node, depth, -math.inf, math.inf, False, heuristic_function, ai_colour, regicide))
	max_value = -math.inf
	for i, value in enumerate(values):
		if value >= max_value:
			max_value = value
	best_move_index = np.random.choice((np.array(values) == max_value).nonzero()[0])
	return sequences[best_move_index]


def get_ai_move_multiprocess(board, ai_colour, depth, heuristic_function, regicide):
	"""
	For the position, find best move by applying minimax w/ alpha-beta pruning.
	Evaluate each move in a seperate process in parallel.
	params:
	  board:
	  ai_colour:
	  depth:
	  heuristic_function:
	"""
	active_colour_after_move = 1 if ai_colour == -1 else -1
	sequences = ch.get_all_move_sequences(board, ai_colour, regicide)
	values = []
	search_calls = []
	for seq in sequences:
		temp_board = copy.deepcopy(board)
		for move in seq:
			ch.update_board(temp_board, move[0], move[1], regicide)
		search_calls.append([Node(temp_board, active_colour_after_move, True, None), depth, -math.inf, math.inf, False, heuristic_function, ai_colour, regicide])
	with multiprocessing.Pool() as pool:
		values = pool.starmap(alpha_beta, search_calls)
	max_value = -math.inf
	for i, value in enumerate(values):
		if value >= max_value:
			max_value = value
	print(sequences)
	print(values)
	print(max_value)
	best_move_index = np.random.choice((np.array(values) == max_value).nonzero()[0])
	return sequences[best_move_index]

