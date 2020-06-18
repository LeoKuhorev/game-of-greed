import random
from collections import Counter


class GameLogic:
    """Game Logic class"""

    @staticmethod
    def calculate_score(dice_roll: tuple) -> int:
        """Calculating score of a given dice roll

        Args:
            dice_roll (tuple): Tuple of integers that represent a dice roll

        Returns:
            int: Roll’s score according to rules of game

        Raises:
            Exception: Not a tuple passed in
            Exception: Tuple value is not integer
        """
        if type(dice_roll) is not tuple:
            raise TypeError('Dice roll must be a tuple')
        for roll in dice_roll:
            if type(roll) is not int:
                raise TypeError('Dice roll value must be integers')
        if len(dice_roll) > 6:
            raise ValueError('The length of tuple must not exceed 6')

        scoring_table = {
            1: (100, True),
            2: (20, False),
            3: (30, False),
            4: (40, False),
            5: (50, True),
            6: (60, False),
        }

        scores = 0
        count = Counter(dice_roll)
        dice_roll = list(dice_roll)

        def score_multiple(number_of_appearance: int) -> None:
            """Helper method. Gets amount of scores for the combination and removes scored values from the pool

            Args:
                number_of_appearance (int): how many times the value appeared in the roll
            """
            if appearance == number_of_appearance:
                nonlocal scores
                scores += (scoring_table[pips][0] * 10) * \
                    (number_of_appearance - 2)
                for _ in range(i):
                    dice_roll.remove(pips)

        if len(count) == 6 or list(count.values()) == [2, 2, 2]:
            scores = 1500
        else:
            for pips, appearance in count.items():
                for i in range(6, 2, -1):
                    if appearance == i:
                        score_multiple(i)

            for dice in dice_roll:
                if scoring_table[dice][1]:
                    scores += scoring_table[dice][0]

        return scores

    @staticmethod
    def roll_dice(number_of_dice: int) -> tuple:
        """Generates a tuple of random values in range 1 - 6

        Args:
            number_of_dice (int): Number of dice to be rolled

        Raises:
            Exception: Value passed in is not an integer
            Exception: Number of dice is out of range

        Returns:
            tuple: Random values in range 1 - 6 for each dice passed in
        """
        if type(number_of_dice) is not int:
            raise TypeError('The number of dice must be an integer')

        if (number_of_dice <= 0 or number_of_dice > 6):
            raise ValueError('The number of dice must be between 1 and 6')

        return tuple(random.randint(1, 6) for _ in range(number_of_dice))


class Banker:
    """Class Banker"""
    shelf_points = 0
    bank_points = 0

    def shelf(self, points: int):
        """Temporarily stores unbanked points

        Args:
            points (int): Number of points to store
        """
        if type(points) is not int:
            raise TypeError('Points must be integer')
        self.shelf_points += points
        return self.shelf_points

    def bank(self) -> int:
        """Permanently stores points from the shelf. Resets shelf points to 0

        Returns:
            int: The amount of points added to total from shelf
        """
        added_points = self.shelf_points
        self.bank_points += self.shelf_points
        self.shelf_points = 0
        return added_points

    def clear_shelf(self):
        """Removes all unbanked points
        """
        self.shelf_points = 0


if __name__ == "__main__":
    print(GameLogic.calculate_score((2, 3, 2, 3, 4, 4,)))
