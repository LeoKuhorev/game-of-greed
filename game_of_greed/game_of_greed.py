import random


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
            if type(roll) is not tuple:
                raise TypeError('Dice roll value must be integers')
        

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

    def shelf(self, points: int):
        """Temporarily stores unbanked points

        Args:
            points (int): Number of points to store
        """
        pass

    def bank(self) -> int:
        """Permanently stores points from the shelf. Resets shelf points to 0

        Returns:
            int: The amount of points added to total from shelf
        """
        pass

    def clear_shelf(self):
        """Removes all unbanked points
        """
        pass





if __name__ == "__main__":
    print(GameLogic.roll_dice(6))
