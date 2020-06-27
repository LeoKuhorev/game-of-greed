from game_of_greed.banker import Banker
from game_of_greed.game_logic import GameLogic

import sys


class GameOfGreed:
    """Game of Greed class"""

    def __init__(self, roll_dice=None):
        self.NUMBER_OF_ROUNDS = 10
        self.bank = Banker()
        self.current_round = 1
        self.number_of_dice_to_roll = 6
        self.roll_dice = roll_dice if roll_dice else GameLogic.roll_dice

        # Game messages
        self.welcome_msg = 'Welcome to Game of Greed'
        self.wanna_play_msg = 'Wanna play? '
        self.invalid_selection_msg = 'Cheater!!! Or possibly made a typo...'
        self.select_dice_msg = 'Enter dice to keep (no spaces), or (q)uit: '
        self.zilch_msg = 'Zilch!!! Round over'
        self.options_msg = '(r)oll again, (b)ank your points or (q)uit '

    def start_game(self) -> None:
        """Print welcome message and ask user if they want to start the game
        """
        print(self.welcome_msg)
        answer = self.validate_answer(input(self.wanna_play_msg), ('y', 'n'))
        if answer == 'y':
            return self.game()
        elif answer == 'n':
            return print('OK. Maybe another time')

    def game(self) -> None:
        """Handle game workflow"""

        print(
            f'Starting round {self.current_round}/{self.NUMBER_OF_ROUNDS}')
        while self.current_round <= self.NUMBER_OF_ROUNDS:
            print(f'Rolling {self.number_of_dice_to_roll} dice...')
            current_roll = self.roll_dice(self.number_of_dice_to_roll)
            print(','.join(str(i) for i in current_roll))

            # If current roll is worth 0 - go to the next round
            if GameLogic.calculate_score(current_roll)[0] == 0:
                print(self.zilch_msg)
                print(
                    f'You banked {self.bank.bank_points} points in round {self.current_round}')
                print(f'Total score is {self.bank.bank_points} points')
                self.bank.clear_shelf()
                self.number_of_dice_to_roll = 6
                self.current_round += 1
                print(
                    f'Starting round {self.current_round}/{self.NUMBER_OF_ROUNDS}')
                continue

            # Handle user dice selection
            selected_dice, all_dice_scored = self.handle_selection(
                current_roll)

            self.number_of_dice_to_roll -= len(selected_dice)

            print(
                f'You have {self.bank.shelf_points} unbanked points and {self.number_of_dice_to_roll} dice remaining')

            answer = self.validate_answer(
                input(self.options_msg), ('r', 'b', 'q'))
            if answer == 'r':
                if self.number_of_dice_to_roll == 0 and all_dice_scored:
                    self.number_of_dice_to_roll = 6
                continue
            elif answer == 'b':
                points = self.bank.bank()
                print(
                    f'You banked {points} points in round {self.current_round}')
                print(f'Total score is {self.bank.bank_points} points')

            self.number_of_dice_to_roll = 6
            self.current_round += 1
            print(
                f'Starting round {self.current_round}/{self.NUMBER_OF_ROUNDS}')

        self.quit()

    def handle_selection(self, current_roll):

        while True:
            # Check if user entry is acceptable (number of dice or quit)
            acceptable_entries = ('1', '2', '3', '4', '5', '6', 'q')
            answer = self.validate_answer(
                input(self.select_dice_msg), acceptable_entries)

            # Check if user entry is a valid selection (dice are present in the current roll)
            while True:
                is_valid = all(str(current_roll).count(dice) >=
                               answer.count(dice) for dice in answer)
                if is_valid:
                    break

                print(self.invalid_selection_msg)
                print(','.join(str(i) for i in current_roll))
                answer = self.validate_answer(
                    input(self.select_dice_msg), acceptable_entries)

            # Calculate score for a valid selection
            valid_selection = tuple([int(i) for i in answer])
            current_score, all_dice_scored, _ = GameLogic.calculate_score(
                valid_selection)

            # Shelf points
            self.bank.shelf(current_score)

            # If current selection is scored more than 0 - return, else ask to select again
            if current_score != 0:
                break

            selection = ', '.join(str(dice) for dice in answer)
            print(
                f'Selection of {selection} gives you 0 points, please try again')

        return (answer, all_dice_scored)

    def validate_answer(self, answer: str, acceptable_options: tuple) -> str:
        """Process user answer and brings it to the consistent format

        Args:
            answer (str): Original user answer
            acceptable_options (tuple): Tuple of acceptable answers

        Returns:
            str: Processed user answer
        """
        while True:
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

            if answer in acceptable_options or any(i in acceptable_options for i in answer):
                break

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
