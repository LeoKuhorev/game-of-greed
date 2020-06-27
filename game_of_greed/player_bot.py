""""
Create a Game of Greed Player Bots
ONLY use public methods
- Game class constructor and play method
- DO NOT INJECT CUSTOM ROLL FUNCTION
- GameLogic, all methods available
"""
import builtins
import re

from game_of_greed.game import GameOfGreed as Game
from game_of_greed.game_logic import GameLogic


class BasePlayer:
    def __init__(self):
        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.total_score = 0

    def reset(self):
        builtins.print = self.old_print
        builtins.input = self.old_input

    def _mock_print(self, *args, **kwargs):
        self.old_print(*args, **kwargs)

    def _mock_input(self, *args, **kwargs):
        return self.old_input(*args, **kwargs)

    @classmethod
    def play(cls, num_games=1):

        mega_total = 0

        for i in range(num_games):
            player = cls()
            game = Game()

            try:
                game.start_game()
            except SystemExit:
                pass

            mega_total += player.total_score
            player.reset()

        print(
            f"{__class__.__name__} {num_games} games (maybe) played with average score of {mega_total // num_games}"
        )


class Naysayer(BasePlayer):
    def _mock_input(self, *args, **kwargs):
        return "n"


class NervousNellie(BasePlayer):
    def __init__(self):
        super().__init__()
        self.roll = None

    def _mock_print(self, *args, **kwargs):
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])

    def _mock_input(self, *args, **kwargs):
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            scorers = self.roll
            keepers = "".join([str(ch) for ch in scorers])
            return keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            return "b"
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")


class PlayerBot(NervousNellie):
    def _mock_print(self, *args, **kwargs):
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])
        elif first_arg.startswith("You have"):
            self.current_points = int(re.findall(r"\d+", first_arg)[0])
        
    def _mock_input(self, *args, **kwargs):
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            self.scorers = GameLogic.get_scorers(self.roll)
            keepers = "".join([str(ch) for ch in self.scorers])
            return keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            self.remaining_dice = len(self.roll) - len(self.scorers)
            if self.remaining_dice == 0:
                self.remaining_dice = 6
            if self.current_points < 500: 
                if self.remaining_dice > 1:
                    return "r"
                else:
                    self.current_points = 0
                    return "b"
            elif self.current_points < 1000:
                if self.remaining_dice > 2:
                    return "r"
                else:
                    self.current_points = 0
                    return "b"
            else:
                if self.remaining_dice > 3:
                    return "r"
            
                else:
                    self.current_points = 0
                    return "b"
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")


if __name__ == "__main__":
    # Naysayer.play(100)
    NervousNellie.play(1000)
    PlayerBot.play(1000)
