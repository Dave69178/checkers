from collections import deque
import copy
import datetime as dt

def create_starting_board():
    """
    return: (list[list : int]) 2D list. 1 = black, 0 = empty, -1 = red.
    """
    return [[0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0]]


class Path:
    """
    Object to store paths within a single turn.
    """
    def __init__(self, start_square=None) -> None:
        """
        params:
          start_squares: (list : int) [row,col]
        """
        if start_square == None:
            self.squares = []
        else:
            self.squares = [start_square]
        self.length = len(self.squares)

    def __str__(self) -> str:
        return str(self.squares)

    def append_left(self, square):
        """
        Add a square to the front of the path.
        params:
          square: (list : int) [row,col]
        """
        self.squares.insert(0, square)
        self.length += 1

    def to_moves_list(self):
        """
        Convert the path to a list of executable moves.
        return: (list[list[list : int]]) [[square0, square1], [square1, square2], ...] where squareN = [row,col], [] indicates no moves
        """
        if len(self.squares) < 2:
            return []
        moves_list = []
        for i in range(len(self.squares) - 1):
            moves_list.append([self.squares[i], self.squares[i+1]])
        return moves_list


def check_end_conditions(board, active_colour):
    """
    Check if game has ended (i.e. has a player won).
    To be called at the end of a turn (active_colour should be the player who has just moved)
    params:
      board: (list[list : [row, col]])
    return: (int) 1 if black wins, -1 if red wins, 0 if still playing
    """
    opponent_colour = 1 if active_colour == -1 else -1
    if get_colour_checker_count(board, opponent_colour) == 0:
        return active_colour
    if does_colour_have_legal_moves(board, opponent_colour):
        return 0
    else:
        return active_colour


def get_colour_checker_count(board, colour):
    """
    Count number of checkers of a given colour
    params:
      board: (list[list : [row, col]])
      colour: (int)
    return: (int)
    """
    count = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] * colour > 0:
                count += 1
    return count


def update_board(board, start_square, end_square):
    """
    Given a legal move, apply the move.
    params:
      board: (list[list : [row, col]])
      start_square: ([int, int]) row,col
      end_square: ([int,int]) row,col
    return: (bool) Whether turn has ended (True), or not (False)
    """
    is_capture = True if abs(start_square[0] - end_square[0]) == 2 else False
    if is_capture:
        return apply_capture_move(board, start_square, end_square)
    else:
        return apply_non_capture_move(board, start_square, end_square)
        

def apply_capture_move(board, start_square, end_square):
    """
    Execute capture move to update board, return value indicating whether turn has ended or not.
    params:
      board: (list[list : [row, col]])
      start_square: ([int, int]) row,col
      end_square: ([int,int]) row,col
    return: (bool) Whether turn has ended (True), or not (False)
    """
    start_r = start_square[0]
    start_c = start_square[1]
    end_r = end_square[0]
    end_c = end_square[1]
    crown = check_for_crowning(board[start_r][start_c], end_square)
    new_checker_val = 0
    if crown:
        new_checker_val = 2 * board[start_r][start_c]
    else:
        new_checker_val = board[start_r][start_c]
    # Execute capture
    board[start_r][start_c], board[end_r][end_c] = 0, new_checker_val
    row_diff = end_square[0] - start_square[0]
    col_diff = end_square[1] - start_square[1]
    board[start_square[0] + row_diff // 2][start_square[1] + col_diff // 2] = 0
    # If crowned, end turn
    if crown:
        return True
    # Check for further captures
    if get_one_step_capture_moves(board, end_square) == []:
        # No further captures, end turn
        return True
    else:
        return False


def apply_non_capture_move(board, start_square, end_square):
    """
    Execute non-capture move to update board, return value indicating whether turn has ended or not.
    params:
      board: (list[list : [row, col]])
      start_square: ([int, int]) row,col
      end_square: ([int,int]) row,col
    return: (bool) Whether turn has ended (True), or not (False)
    """
    start_r = start_square[0]
    start_c = start_square[1]
    end_r = end_square[0]
    end_c = end_square[1]
    crown = check_for_crowning(board[start_r][start_c], end_square)
    new_checker_val = 0
    if crown:
        new_checker_val = 2 * board[start_r][start_c]
    else:
        new_checker_val = board[start_r][start_c]
    board[start_r][start_c], board[end_r][end_c] = 0, new_checker_val
    return True


def check_for_crowning(checker, end_square):
    """
    Given a legal move, check if the checker should be crowned.
    params:
      checker: (int)
      end_square: ([int,int]) row,col
    return: (bool) Whether checker should be crowned (True), or not (False)
    """
    if abs(checker) == 2:
        return False
    else:
        if checker > 0:
            if end_square[0] == 7:
                return True
            else:
                return False
        elif checker < 0:
            if end_square[0] == 0:
                return True
            else:
                return False
        else:
            raise Exception("No checker in start square")


def is_move_legal(board, legal_moves, active_colour, start_square, end_square):
    """
    Check whether a given move is legal. Indicate why not if it isn't.
    params:
      board: (list[list : int])
      legal_moves: (list[list[list : [row,col]]]) Same as a board, except the value in each board position is the legal moves for that square
      active_colour: (int)
      start_square: ([int, int]) row,col
      end_square: ([int,int]) row,col
    return: (bool)
    """
    if board[start_square[0]][start_square[1]] * active_colour < 0:
        print("You can't move your opponent's pieces!")
        return False
    elif board[start_square[0]][start_square[1]] * active_colour == 0:
        print("There is no checker to move.")
        return False
    else:
        # Check if legal move for piece
        if end_square in legal_moves[start_square[0]][start_square[1]]:
            return True
        else:
            print("This is not a legal move for the selected checker.")
            return False


def does_colour_have_legal_moves(board, colour):
    """
    Doas a given colour have any moves
    params:
      board: (list[list : [row, col]])
      colour: (int)
    return: (int) True if they have at least one legal move, false otherwise
    """
    for row in range(8):
        for col in range(8):
            if board[row][col] * colour > 0:
                if get_one_step_moves_for_piece(board, [row,col]) != []:
                    return True
    return False


def get_all_one_step_moves_for_colour(board, colour):
    """
    Assuming the colour is active, get all legal (one-step) moves.
    params:
      board: (list[list : [row, col]])
      colour: (int)
    return: (list[list[list : [row,col]]]) Same as a board, except the value in each board position is the legal moves for that square
    """
    legal_moves = [[[] for col in range(8)] for row in range(8)]
    capture_exists = False
    for row in range(8):
        for col in range(8):
            if board[row][col] * colour > 0:
                capture_moves = get_one_step_capture_moves(board, [row,col])
                if capture_moves != []:
                    legal_moves[row][col] = capture_moves
                    capture_exists = True
    if not capture_exists:
        for row in range(8):
            for col in range(8):
                if board[row][col] * colour > 0:
                    non_capture_moves = get_non_capture_moves(board, [row,col])
                    if non_capture_moves != []:
                        legal_moves[row][col] = non_capture_moves
    return legal_moves


def get_all_turn_end_positions(board, colour):
    """
    Get every possible board state after turn is finished.
    params:
      board: (list[list : [row, col]])
      colour: (int)
    return: (list : board), [] if no positions (game has ended)
    """
    moves_store = get_all_move_sequences(board, colour)
    # Get board position after each move
    positions = []
    for sequence in moves_store:
        temp_board = copy.deepcopy(board)
        for move in sequence:
            update_board(temp_board, move[0], move[1])
        positions.append(temp_board)
    return positions


def get_all_move_sequences(board, colour):
    """
    Get every move sequence for board position and colour.
    params:
      board: (list[list : [row, col]])
      colour: (int)
    return: (list : sequence), 
      Breakdown of sequence:
            sequence (list : moves), moves (list : squares), squares (list : int)
    """
    def end_squares_to_moves(start_square, end_squares):
        """
        Given a single start square, and a list of end squares, convert to list of moves.
        params:
          start_square: ([int, int]) row,col
          end_squares: (list : [[[int,int],[int,int]]]) list of [[[row,col], [row,col]]]'s list of sequences (sequence is a list of moves, move = [start_square, end_square])
        """
        moves = []
        for move in end_squares:
            moves.append([[start_square, move]])
        return moves

    moves_store = []
    # Get capture moves
    is_captures = False
    for row in range(8):
        for col in range(8):
            if board[row][col] * colour > 0:
                capture_paths = get_multi_capture_moves_for_square(board, [row,col])
                if len(capture_paths) > 0:
                    # Force captures
                    is_captures = True
                    for path in capture_paths:
                        moves_store.append(path.to_moves_list())
    # Get non-capture moves if there are no captures
    if not is_captures:
        for row in range(8):
            for col in range(8):
                if board[row][col] * colour > 0:
                    non_capture_moves = get_non_capture_moves(board, [row,col])
                    if non_capture_moves != []:
                        moves_store += end_squares_to_moves([row, col], non_capture_moves)
    return moves_store


def get_multi_capture_moves_for_square(board, start_square):
    """
    Given a square, find all of the different capture moves (paths) possible.
    params:
      board: (list[list : int])
      start_square: ([int, int]) row,col
    return: (list : Path) A list of Path objects, [] for no paths
    """
    class Node:
        """
        Nodes for search to find all capture paths
        """
        def __init__(self, board, visited, parent, square, end_turn=False) -> None:
            self.board = board
            self.visited = visited
            self.parent = parent
            self.square = square
            self.end_turn = end_turn
    moves_store = []
    queue = deque()
    origin = Node(board, True, None, start_square)
    queue.append(origin)
    while len(queue) > 0:
        v = queue.pop()
        if v.end_turn:
            children = []
        else:
            children = get_one_step_capture_moves(v.board, v.square)
        if children == []:
            path = Path()
            while v.parent != None:
                path.append_left(v.square)
                v = v.parent
            # If path has length 0, there were no captures
            if path.length > 0:
                # Add origin square to path
                path.append_left(v.square)
                moves_store.append(path)
        else:
            for child in children:
                temp = copy.deepcopy(v.board)
                if update_board(temp, v.square, child):
                    # End turn
                    queue.appendleft(Node(temp, False, v, child, True))
                    continue
                else:
                    queue.appendleft(Node(temp, False, v, child))
    return moves_store


def get_one_step_moves_for_piece(board, start_square):
    """
    Assuming it is the given colour's turn to move, get all one step moves for that piece.
    params:
      board: (list[list : int])
      start_square: ([int, int]) row,col
    """
    capture_moves = get_one_step_capture_moves(board, start_square)
    if capture_moves != []:
        # Force capture
        return capture_moves
    else:
        return get_non_capture_moves(board, start_square)


def get_non_capture_moves(board, start_square):
    """
    Assuming it is the given colour's turn to move, get all non-capture moves for that piece.
    params:
      board: (list[list : int])
      start_square: ([int, int]) row,col
    return: (list[list : [int, int]]), List containing end_squares of each legal non-capture, empty list if no moves
    """
    start_row, start_col = start_square[0], start_square[1]
    checker = board[start_row][start_col]
    # Get possible non-capture moves that are on the board for that checker
    non_capture_moves = get_non_capture_squares(start_square, checker)
    remove_moves = set()

    # Check end square is empty
    for ind, move in enumerate(non_capture_moves):
        # Capture is [row,col]
        end_square = board[move[0]][move[1]]
        if end_square == 0:
            continue
        else:
            # Piece blocking move
            remove_moves.add(ind)
    
    remove_moves = list(remove_moves)
    return [move for ind, move in enumerate(non_capture_moves) if ind not in remove_moves]


def get_non_capture_squares(start_square, checker):
    """
    For a given square and piece, get each theoretically possible non-capture move.
    params:
      start_square: ([int,int])
      checker: (int) 0 = empty, 1 = black checker, 2 = black king, -1 = red checker, -2 = red king
    return: (list[list : [row,col]]) List of possible non-capture move squares
    """
    start_row, start_col = start_square[0], start_square[1]
    non_capture_moves = [[start_row + 1, start_col - 1],
                          [start_row + 1, start_col + 1],
                           [start_row - 1, start_col - 1],
                            [start_row - 1, start_col + 1]]
    remove_moves = set()
    # Remove moves off board
    for ind, move in enumerate(non_capture_moves):
        # move is [row,col]
        if is_move_on_board(move):
            continue
        else:
            remove_moves.add(ind)
    if checker > 0:
        # Black checker
        if checker != 2:
            # Not King
            remove_moves.add(2)
            remove_moves.add(3)
    elif checker < 0:
        # Red checker
        if checker != -2:
            # Not King
            remove_moves.add(0)
            remove_moves.add(1)
    else:
        raise Exception("No checker in start square")
    remove_moves = list(remove_moves)
    return [move for ind, move in enumerate(non_capture_moves) if ind not in remove_moves]


def get_one_step_capture_moves(board, start_square):
    """
    Assuming it is the given colour's turn to move, get all one step capture moves for that piece.
    params:
      board: (list[list : int])
      start_square: ([int, int]) row,col
    return: (list[list : [int, int]]), List containing end_squares of each legal capture, empty list if no captures
    """
    start_row, start_col = start_square[0], start_square[1]
    checker = board[start_row][start_col]
    # Get possible capture moves that are on the board
    capture_moves = get_one_step_capture_squares(start_square, checker)
    remove_moves = set()

    # Check end square is empty
    for ind, capture in enumerate(capture_moves):
        # Capture is [row,col]
        end_square = board[capture[0]][capture[1]]
        if end_square == 0:
            continue
        else:
            # Piece blocking capture
            remove_moves.add(ind)

    # Check there is opponent piece to capture
    for ind, capture in enumerate(capture_moves):
        # Capture is [row,col]
        if is_piece_to_capture(board, checker, start_square, capture):
            continue
        else:
            remove_moves.add(ind)
    remove_moves = list(remove_moves)
    return [move for ind, move in enumerate(capture_moves) if ind not in remove_moves]


def get_one_step_capture_squares(start_square, checker):
    """
    For a given square and piece, get each theoretically possible capture move.
    params:
      start_square: ([int,int])
      checker: (int) 0 = empty, 1 = black checker, 2 = black king, -1 = red checker, -2 = red king
    return: (list[list : [row,col]]) List of possible capture move squares
    """
    start_row, start_col = start_square[0], start_square[1]
    capture_moves = [[start_row + 2, start_col - 2],
                      [start_row + 2, start_col + 2],
                       [start_row - 2, start_col - 2],
                        [start_row - 2, start_col + 2]]
    remove_moves = set()
    # Remove moves off board
    for ind, move in enumerate(capture_moves):
        # move is [row,col]
        if is_move_on_board(move):
            continue
        else:
            remove_moves.add(ind)
    if checker > 0:
        # Black checker
        if checker != 2:
            # Not King
            remove_moves.add(2)
            remove_moves.add(3)
    elif checker < 0:
        # Red checker
        if checker != -2:
            # Not King
            remove_moves.add(0)
            remove_moves.add(1)
    else:
        raise Exception("No checker in start square")
    remove_moves = list(remove_moves)
    return [move for ind, move in enumerate(capture_moves) if ind not in remove_moves]


def is_move_on_board(end_square):
    """
    Is the end square on the board.
    params:
      end_square: ([int, int]) row,col
    return: (bool)
    """
    for axis_index in end_square:
            # axis is a row or col index
            if axis_index < 0 or axis_index > 7:
                # Move is off board
                return False
    return True


def is_piece_to_capture(board, checker, start_square, end_square):
    """
    For a given position and capture move, check that there is an opponent piece to capture.
    params:
      board: (list[list : int])
      start_square: ([int, int]) row,col
      end_square: ([int, int]) row,col
    return: (bool)
    """
    row_diff = end_square[0] - start_square[0]
    col_diff = end_square[1] - start_square[1]
    if board[start_square[0] + row_diff // 2][start_square[1] + col_diff // 2] * checker < 0:
        # Opponent piece
        return True
    else:
        # Not opponent piece
        return False
    

def log_message(message_log, message):
    log_time = dt.datetime.now().time()
    message_log.append(f"{str(log_time)[0:8]}: {message}")

