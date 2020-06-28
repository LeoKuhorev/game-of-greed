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
    """Provided Base Player class"""

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
            f"{cls.__name__}: {num_games} games played with average score of {mega_total // (num_games * game.NUMBER_OF_ROUNDS)} per game"
        )


class NervousNellie(BasePlayer):
    """Provided Nervous Nellie bot that always scores the first roll and banks right away
    """

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


class PlayerBot(BasePlayer):
    """Bot for the Game Of Greed game
    """

    def __init__(self):
        super().__init__()
        self.roll = None
        self.current_points = None
        self.scorers = None
        self.remaining_dice = None

    def _mock_print(self, *args, **kwargs):
        """Capture STDOUT prompts and save roll, current_points and total score of an instance
        """
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])
        elif first_arg.startswith("You have"):
            self.current_points = int(re.findall(r"\d+", first_arg)[0])

    def _mock_input(self, *args, **kwargs):
        """Capture STDINPUT prompts and return corresponding answer

        Raises:
            ValueError: If unknown prompt message is present

        Returns:
            Corresponding answer to handle game logic
        """
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            self.scorers = GameLogic.get_scorers(self.roll)

            all_dice_scored = GameLogic.calculate_score(self.roll)[1]
            if all_dice_scored:
                self.scorers = self.roll

            # If the entire roll (5 or 6 dice) is scored under 300 points, select only 1 dice
            elif GameLogic.calculate_score(self.scorers)[0] < 300 and len(self.roll) > 4:
                if 1 in self.scorers:
                    self.scorers = (1, )
                elif 5 in self.scorers:
                    self.scorers = (5, )

            keepers = "".join([str(ch) for ch in self.scorers])
            return keepers

        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            self.remaining_dice = len(self.roll) - len(self.scorers)

            # Reset when all dice are scored
            if self.remaining_dice == 0:
                self.remaining_dice = 6

            combinations = (
                {'dice_left': 1, 'min_points': 250},
                {'dice_left': 2, 'min_points': 300},
                {'dice_left': 3, 'min_points': 400},
                {'dice_left': 4, 'min_points': 700},
                {'dice_left': 5, 'min_points': 1500},
            )

            # Keep rolling if the points are below the minimum for a particular number of dice left
            for combination in combinations:
                if self.remaining_dice == combination['dice_left']:
                    if self.current_points > combination['min_points']:
                        self.current_points = 0
                        return 'b'
            return 'r'

        else:
            raise ValueError(f"Unrecognized prompt {prompt}")


if __name__ == "__main__":
    NervousNellie.play(10000)
    PlayerBot.play(10000)
