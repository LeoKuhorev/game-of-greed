class Banker:
    """Class Banker"""

    def __init__(self):
        self.shelf_points = 0
        self.bank_points = 0

    def __repr__(self):
        return 'Banker()'

    def __str__(self):
        return f'shelf poins: {self.shelf_points}, bank points: {self.bank_points}'

    def shelf(self, points: int):
        """Temporarily stores unbanked points

        Args:
            points (int): Number of points to store

        Returns:
            int: Current shelf points amount
        """
        if type(points) is not int:
            raise TypeError('Points must be integer')
        self.shelf_points += points
        return self.shelf_points

    def clear_shelf(self):
        """Removes all unbanked points
        """
        self.shelf_points = 0

    def bank(self) -> int:
        """Permanently stores points from the shelf. Resets shelf points to 0

        Returns:
            int: The amount of points added to total from shelf
        """
        added_points = self.shelf_points
        self.bank_points += self.shelf_points
        self.clear_shelf()
        return added_points
