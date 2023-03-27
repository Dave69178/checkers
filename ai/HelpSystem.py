import game.CheckersHelper as ch
import ai.Search as s
import ai.Heuristics as h

def get_help_message_for_position(game):
    """
    Given the current game state, return a string message advising the player.
    params:
      game: (Checkers)
    return: (str)
    """
    move = str(s.get_ai_move_multiprocess(game.board, game.active_colour, 5, h.checker_value_difference, game.regicide))
    ch.log_message(game.game_log, f"Consider the move: {move}")