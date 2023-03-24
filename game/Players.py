import ai.Heuristics as heur

class Player:
    def __init__(self, colour) -> None:
        """
        params:
          colour: (int) colour checker the player controls, -1 = red, 1 = black
        """
        self.colour = colour


class Human(Player):
    def __init__(self, colour) -> None:
        super().__init__(colour)


class AI(Player):
    def __init__(self, colour, difficulty) -> None:
        super().__init__(colour)
        self.difficulty = difficulty
        if difficulty == 1:
            self.depth = 1
            self.heuristic_function = heur.checker_value_difference
        elif difficulty == 2:
            self.depth = 3
            self.heuristic_function = heur.checker_value_difference
        elif difficulty == 3:
            self.depth = 7
            self.heuristic_function = heur.checker_value_difference
        else:
            raise Exception("Difficulty must be 1,2 or 3")


