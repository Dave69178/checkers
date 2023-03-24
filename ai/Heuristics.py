import math

def checker_value_difference(board, ai_colour):
	"""
	Count number of checkers (kings count as 2). Return diff in ai and opposition numbers
	return: (int)
	"""
	ai_value = 0
	opponent_value = 0
	opponent_colour = 1 if ai_colour == -1 else -1
	for row in range(8):
		for col in range(8):
			checker = board[row][col]
			if checker == 0:
				continue
			elif checker * ai_colour > 0:
				ai_value += abs(checker)
			elif checker * opponent_colour > 0:
				opponent_value += abs(checker)
	return ai_value - opponent_value


def checker_value_ratio(board, ai_colour):
	"""
	Count number of checkers (kings count as 2). Return ratio of ai and opposition numbers
	return: (int)
	"""
	ai_value = 0
	opponent_value = 0
	opponent_colour = 1 if ai_colour == -1 else -1
	for row in range(8):
		for col in range(8):
			checker = board[row][col]
			if checker == 0:
				continue
			elif checker * ai_colour > 0:
				ai_value += abs(checker)
			elif checker * opponent_colour > 0:
				opponent_value += abs(checker)
	try:
		pos_value = ai_value / opponent_value
	except ZeroDivisionError:
		print("Zero division Error in heuristic")
		pos_value = math.inf
	
	return pos_value
