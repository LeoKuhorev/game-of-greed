from banker import Banker
from game_logic import GameLogic

from collections import Counter


class GameOfGreed:

    def __init__(self):
        self.NUMBER_OF_ROUNDS = 10
        self.bank = Banker()
        self.welcome_message = 'Welcome to Game of Greed'
        self.wanna_play_message = 'Wanna play? y/n '
        self.incorrect_dice_message = 'Cheater!!! Or possibly made a typo...'
        self.select_dice_message = 'Enter dice to keep (no spaces), or (q)uit: '

    def validate_answer(self, answer):
        if answer.lower() == 'yes' or answer.lower() == 'y':
            answer = 'y'
        elif answer.lower() == 'no' or answer.lower() == 'n':
            answer = 'n'
        elif answer.lower() == 'roll' or answer.lower() == 'r':
            answer = 'r'
        elif answer.lower() == 'quit' or answer.lower() == 'q':
            answer = 'q'
        elif answer.lower() == 'bank' or answer.lower() == 'b':
            answer = 'b'

        return answer

    def start_game(self):

        print(self.welcome_message)
        answer = self.validate_answer(input(self.wanna_play_message))

        while answer != 'y' or answer != 'n':
            if answer == 'y':
                return self.start_rounds()
            elif answer == 'n':
                return print('OK. Maybe another time')
            answer = self.validate_answer(
                input(f'Sorry, {answer} is not a valid option. {self.wanna_play_message}'))

    def start_rounds(self):
        rounds = 1
        dice = 6

        while rounds <= self.NUMBER_OF_ROUNDS:
            print(f'Starting round {rounds}/{self.NUMBER_OF_ROUNDS}')
            print(f'Rolling {dice} dice...')
            result = GameLogic.roll_dice(dice)
            print(result)

            score = 0
            while score == 0:
                answer = self.validate_answer(input(self.select_dice_message))
                if answer == 'q':
                    return self.quit()
                selected_dice = self.select_dice(answer, result)
                score = GameLogic.calculate_score(selected_dice)
                shelf_points = self.bank.shelf(score)

            dice -= len(answer)
            print(
                f'You have {shelf_points} unbanked points and {dice} dice remaining')

            answer = self.validate_answer(
                input('(r)oll again, (b)ank your points or (q)uit q '))
            if answer == 'q':
                break
            elif answer == 'r':
                if dice == 0:
                    dice = 6
                continue
            elif answer == 'b':
                dice = 6
                points = self.bank.bank()
                print(f'You banked {points} points in round {rounds}')

            rounds += 1

        self.quit()

    def select_dice(self, answer, result):
        output = []
        for dice in answer:
            dice = int(dice)
            if result.count(dice) > output.count(dice):
                output.append(dice)
            else:
                answer = self.validate_answer(input(
                    f'{self.incorrect_dice_message} {self.select_dice_message}'))

        return tuple(output)

    def quit(self):
        return print(f'Thanks for playing. You earned {self.bank.bank_points} points')


if __name__ == "__main__":
    new_game = GameOfGreed()
    new_game.start_game()
