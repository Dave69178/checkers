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
		pos_value = ai_value / (opponent_value + ai_value)
	except ZeroDivisionError:
		print("Zero division Error in heuristic")
		pos_value = math.inf
	return pos_value




def checker_position_value(board, ai_colour):
	"""
	Give each piece a value depending on position and king status
	"""
	eval = 0
	for row in range(8):
		for col in range(8):
			checker_value = 0
			checker = board[row][col]
			if checker * ai_colour > 0:
				if checker > 0:
					checker_value += 1
					if checker == 1:
						# Non-king checker near to crowning
						if row > 4:
							checker_value += 1
					else:
						# Crowned checker
						checker_value += 2
						if row < 7:
							# Dumb method to incentivise non-trapped King 
							checker_value += 1
				else:
					checker_value += 1
					if checker == -1:
						if row < 3:
							checker_value += 1
					else:
						checker_value += 2
						if row > 0:
							checker_value += 1
				eval += checker_value
			elif checker * ai_colour < 0:
				if checker > 0:
					checker_value += 1
					if checker == 1:
						# Non-king checker near to crowning
						if row > 4:
							checker_value += 1
					else:
						# Crowned checker
						checker_value += 2
						if row < 7:
							# Dumb method to incentivise non-trapped King 
							checker_value += 1
				else:
					checker_value +=1
					if checker == -1:
						if row < 3:
							checker_value += 1
					else:
						checker_value += 2
						if row > 0:
							checker_value += 1
				eval -= checker_value
	return eval


def unstoppable_crown_count(board, ai_colour):
	"""
	Count the number of opponent checkers that can't be stopped from crowning.
	"""
	start_row = 0 if ai_colour == 1 else 3
	end_row = 4 if ai_colour == 1 else 7
	unstoppable_count = 0
	for row in range(8):
		if row >= start_row and row <= end_row:
			for col in range(8):
				if board[row][col] * ai_colour < 0:
					if abs(board[row][col]) == 2:
						continue
					if is_checker_crown_unstoppable(board, [row,col]):
						unstoppable_count += 1
	return unstoppable_count


def is_checker_crown_unstoppable(board, square):
	"""
	Check if there are any checkers that can capture the given checker before it crowns. (Simple version, can be cases where it gives wrong result)
	"""
	row = square[0]
	col = square[1]
	checker = board[row][col]
	colour = 1 if checker > 0 else -1
	opponent_colour = 1 if colour == -1 else -1
	rows_to_check = range(row,8) if colour == 1 else range(row, -1, -1)
	for temp_row in rows_to_check:
		if temp_row == row:
			if col + 2 > 7 or col - 2 < 0:
				continue
			if board[row][col+2] == 2 * opponent_colour or board[row][col-2] == 2 * opponent_colour:
				return False
		elif temp_row == row + colour:
			continue
		elif temp_row == row + 2 * colour:
			if board[temp_row][col] * opponent_colour > 0:
				return False
		elif temp_row == row + 3 * colour:
			if col + 1 > 7 or col - 1 < 0:
				continue
			if board[temp_row][col + 1] * opponent_colour > 0 or board[temp_row][col - 1] * opponent_colour > 0:
				return False
		elif temp_row == row + 4 * colour:
			if col + 2 > 7 or col - 2 < 0:
				continue
			if board[temp_row][col] * opponent_colour > 0 or board[temp_row][col - 2] * opponent_colour > 0 or board[temp_row][col + 2] * opponent_colour > 0:
				return False
	return True


def combination_heurustic(board, ai_colour):
	return checker_value_ratio(board, ai_colour) - unstoppable_crown_count(board, ai_colour)


