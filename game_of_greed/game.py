from game_of_greed.banker import Banker
from game_of_greed.game_logic import GameLogic

from collections import Counter
import sys


class GameOfGreed:
    """Game of Greed class"""

    def __init__(self, roll_dice=None):
        self.NUMBER_OF_ROUNDS = 10
        self.bank = Banker()

        # Game messages
        self.welcome_msg = 'Welcome to Game of Greed'
        self.wanna_play_msg = 'Wanna play? '
        self.invalid_selection_msg = 'Cheater!!! Or possibly made a typo...'
        self.select_dice_msg = 'Enter dice to keep (no spaces), or (q)uit: '
        self.zero_point_roll_msg = 'Your current roll is worth 0 points. You\'ve lost all your unbanked points in this round'
        self.options_msg = '(r)oll again, (b)ank your points or (q)uit '

    def start_game(self) -> None:
        """Print welcome message and ask user if they want to start the game
        """
        print(self.welcome_msg)
        answer = self.validate_answer(
            input(self.wanna_play_msg), ('y', 'n', 'q'))
        if answer == 'y':
            return self.game()
        elif answer == 'n':
            return print('OK. Maybe another time')

    def game(self) -> None:
        """Handle game workflow"""
        current_round = 1
        dice_to_roll = 6

        while current_round <= self.NUMBER_OF_ROUNDS:
            print(f'Starting round {current_round}/{self.NUMBER_OF_ROUNDS}')
            print(f'Rolling {dice_to_roll} dice...')
            current_roll = GameLogic.roll_dice(dice_to_roll)
            print(','.join(str(i) for i in current_roll))

            # If current roll is worth 0 - go to the next round
            if GameLogic.calculate_score(current_roll) == 0:
                print(self.zero_point_roll_msg)
                dice_to_roll = 6
                current_round += 1
                continue

            current_score = 0
            while current_score == 0:
                answer = self.validate_answer(
                    input(self.select_dice_msg), ('1', '2', '3', '4', '5', '6', 'q'))

                # Validate user selection
                valid_selection = self.validate_selection(answer, current_roll)
                while not valid_selection:
                    print(f'{self.invalid_selection_msg}')
                    print(','.join(str(i) for i in current_roll))
                    answer = self.validate_answer(
                        input(self.select_dice_msg), ('1', '2', '3', '4', '5', '6', 'q'))
                    valid_selection = self.validate_selection(
                        answer, current_roll)

                # Calculate score for a valid selection
                current_score = GameLogic.calculate_score(
                    self.convert_selection(answer))

                # Shelf points
                self.bank.shelf(current_score)

                # If current selection is worth 0 - ask user to select again
                if current_score == 0:
                    selection = ', '.join(str(dice) for dice in answer)
                    print(
                        f'Selection of {selection} gives you 0 points, please try again')

            dice_to_roll -= len(answer)
            print(
                f'You have {self.bank.shelf_points} unbanked points and {dice_to_roll} dice remaining')

            answer = self.validate_answer(
                input(self.options_msg), ('r', 'b', 'q'))
            if answer == 'r':
                if dice_to_roll == 0:
                    dice_to_roll = 6
                continue
            elif answer == 'b':
                dice_to_roll = 6
                points = self.bank.bank()
                print(f'You banked {points} points in round {current_round}')
                print(f'Total score is {self.bank.bank_points} points')

            current_round += 1

        self.quit()

    def validate_selection(self, selection: str, roll: tuple) -> bool:
        """Checks if user wants to proceed with the dice that are present in the given roll

        Args:
            selection (str): Dice that user decided to score
            roll (tuple): Current roll

        Returns:
            bool: Whether all dice are present in current roll
        """
        is_valid = True
        for dice in selection:
            if str(roll).count(dice) < selection.count(dice):
                is_valid = False

        return is_valid

    def convert_selection(self, valid_selection: str) -> tuple:
        """Converts user selected dice into a tuple of integers

        Args:
            valid_selection (str): User dice selection

        Returns:
            tuple: Tuple of integers of the same user selection
        """
        return tuple([int(i) for i in valid_selection])

    def validate_answer(self, answer: str, acceptable_options: tuple) -> str:
        """Process user answer and brings it to the consistent format

        Args:
            answer (str): Original user answer

        Returns:
            str: Processed user answer
        """
        while answer not in acceptable_options:
            if answer.lower() == 'yes' or answer.lower() == 'y':
                answer = 'y'
            elif answer.lower() == 'no' or answer.lower() == 'n':
                answer = 'n'
            elif answer.lower() == 'roll' or answer.lower() == 'r':
                answer = 'r'
            elif answer.lower() == 'bank' or answer.lower() == 'b':
                answer = 'b'
            elif answer.lower() == 'quit' or answer.lower() == 'q':
                self.quit()
            answer = input(self.invalid_selection_msg)

        return answer

    def quit(self):
        """Shows final message and exits the program
        """
        print(f'Total score is {self.bank.bank_points} points')
        print(f'Thanks for playing. You earned {self.bank.bank_points} points')
        sys.exit()


if __name__ == "__main__":
    new_game = GameOfGreed()
    new_game.start_game()
