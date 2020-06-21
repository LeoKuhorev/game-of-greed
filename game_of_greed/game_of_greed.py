from banker import Banker
from game_logic import GameLogic

from collections import Counter
import sys


class GameOfGreed:
    """Game of Greed class"""

    def __init__(self):
        self.NUMBER_OF_ROUNDS = 10
        self.bank = Banker()
        self.welcome_msg = 'Welcome to Game of Greed'
        self.wanna_play_msg = 'Wanna play? y/n '
        self.invalid_selection_msg = 'Cheater!!! Or possibly made a typo...'
        self.select_dice_msg = 'Enter dice to keep (no spaces), or (q)uit: '

    def start_game(self) -> None:
        """Prints welcome message and asks user if they want to start the game
        """
        print(self.welcome_msg)
        answer = self.validate_answer(input(self.wanna_play_msg))

        while answer != 'y' or answer != 'n':
            if answer == 'y':
                return self.game()
            elif answer == 'n':
                return print('OK. Maybe another time')
            answer = self.validate_answer(
                input(f'Sorry, {answer} is not a valid option. {self.wanna_play_msg}'))

    def game(self) -> None:
        """Handles game workflow"""
        rounds = 1
        dice = 6

        while rounds <= self.NUMBER_OF_ROUNDS:
            print(f'Starting round {rounds}/{self.NUMBER_OF_ROUNDS}')
            print(f'Rolling {dice} dice...')
            current_roll = GameLogic.roll_dice(dice)
            print(current_roll)

            # If current roll is worth 0 - go to the next round
            if GameLogic.calculate_score(current_roll) == 0:
                print(
                    'Your current roll is worth 0 points. You\'ve lost all your unbanked points in this round')
                dice = 6
                continue

            current_score = 0
            while current_score == 0:
                answer = self.validate_answer(input(self.select_dice_msg))

                # Validate user selection
                valid_selection = self.validate_selection(answer, current_roll)
                while not valid_selection:
                    answer = self.validate_answer(
                        input(f'{self.invalid_selection_msg} {self.select_dice_msg}'))
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

            dice -= len(answer)
            print(
                f'You have {self.bank.shelf_points} unbanked points and {dice} dice remaining')

            answer = self.validate_answer(
                input('(r)oll again, (b)ank your points or (q)uit q '))
            if answer == 'r':
                if dice == 0:
                    dice = 6
                continue
            elif answer == 'b':
                dice = 6
                points = self.bank.bank()
                print(f'You banked {points} points in round {rounds}')

            rounds += 1

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

    def validate_answer(self, answer: str) -> str:
        """Process user answer and brings it to the consistent format

        Args:
            answer (str): Original user answer

        Returns:
            str: Processed user answer
        """
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

        return answer

    def quit(self):
        """Shows final message and exits the program
        """
        print(f'Thanks for playing. You earned {self.bank.bank_points} points')
        sys.exit()


if __name__ == "__main__":
    new_game = GameOfGreed()
    new_game.start_game()
