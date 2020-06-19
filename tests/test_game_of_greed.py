import pytest
from collections import Counter

from game_of_greed import __version__
from game_of_greed.game_of_greed import Banker, GameLogic


def test_proof_of_life():
    assert __version__ == '0.1.0'


class TestGameLogic:
    """Tests for the Game Logic class and its methods
    """
    @pytest.fixture()
    def gl(self):
        return GameLogic()

    def test_gl_instance(self):
        """Check class instantiation"""
        assert GameLogic()

    def test_gl_calculate_score_type_error_1(self):
        """Test if the method raises TypeError when not a tuple passed in"""
        with pytest.raises(TypeError) as err:
            assert GameLogic.calculate_score([1, 2, 3])
        assert str(err.value) == "Dice roll must be a tuple"

    def test_gl_calculate_score_type_error_2(self):
        """Test if the method raises TypeError when one of the tuple elements is not an integer"""
        with pytest.raises(TypeError) as err:
            assert GameLogic.calculate_score((1, 2, 'banana'))
        assert str(err.value) == "Dice roll value must be integers"

    @pytest.mark.parametrize('roll, result', [
        # zilch
        ((2, 3, 4, 6), 0),
        ((4, 4, 2, 3), 0),
        ((6, 3, 2, 4), 0),

        # ones & leftover_ones
        ((1,), 100),
        ((1, 1), 200),
        ((1, 1, 1), 1000),
        ((1, 1, 1, 1), 2000),
        ((1, 1, 1, 1, 1), 3000),
        ((1, 1, 1, 1, 1, 1), 4000),

        # twos
        ((2,), 0),
        ((2, 2), 0),
        ((2, 2, 2), 200),
        ((2, 2, 2, 2), 400),
        ((2, 2, 2, 2, 2), 600),
        ((2, 2, 2, 2, 2, 2), 800),

        # threes
        ((3,), 0),
        ((3, 3), 0),
        ((3, 3, 3), 300),
        ((3, 3, 3, 3), 600),
        ((3, 3, 3, 3, 3), 900),
        ((3, 3, 3, 3, 3, 3), 1200),

        # fours
        ((4,), 0),
        ((4, 4), 0),
        ((4, 4, 4), 400),
        ((4, 4, 4, 4), 800),
        ((4, 4, 4, 4, 4), 1200),
        ((4, 4, 4, 4, 4, 4), 1600),

        # fives & leftover_fives
        ((5,), 50),
        ((5, 5), 100),
        ((5, 5, 5), 500),
        ((5, 5, 5, 5), 1000),
        ((5, 5, 5, 5, 5), 1500),
        ((5, 5, 5, 5, 5, 5), 2000),

        # sixes
        ((6,), 0),
        ((6, 6), 0),
        ((6, 6, 6), 600),
        ((6, 6, 6, 6), 1200),
        ((6, 6, 6, 6, 6), 1800),
        ((6, 6, 6, 6, 6, 6), 2400),

        # straight
        ((1, 2, 3, 4, 5, 6), 1500),
        ((5, 1, 4, 2, 6, 3), 1500),
        ((6, 5, 4, 3, 2, 1), 1500),

        # three pairs
        ((1, 2, 3, 3, 2, 1), 1500),
        ((5, 5, 4, 2, 4, 2), 1500),
        ((2, 2, 4, 4, 3, 3), 1500),

        # two_trios
        ((1, 1, 1, 2, 2, 2), 1200),
        ((3, 3, 3, 4, 4, 4), 700),
        ((5, 5, 5, 6, 6, 6), 1100),

    ])
    def test_gl_calculate_score(self, roll, result):
        """Test if the method calculates correct number of scores
        Args:
            roll (tuple): roll combination
            result (int): points result
        """
        assert GameLogic.calculate_score(roll) == result

    def test_gl_roll_dice_type_error(self):
        """Test if the method raises TypeError if not an integer passed in"""
        with pytest.raises(TypeError) as err:
            assert GameLogic.roll_dice(1.5)
        assert str(err.value) == "The number of dice must be an integer"

    def test_gl_roll_dice_value_error_1(self):
        """Test if the method raises ValueError if the passed in integer is out of range"""
        with pytest.raises(ValueError) as err:
            assert GameLogic.roll_dice(0)
        assert str(err.value) == "The number of dice must be between 1 and 6"

    def test_gl_roll_dice_pass_1(self):
        """Test if the method returns a tuple"""
        assert type(GameLogic.roll_dice(2)) is tuple

    def test_gl_roll_dice_pass_2(self):
        """Test if the method returns all values in specified range (1 - 6)
        """
        results = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for _ in range(10000):
            roll = Counter(GameLogic.roll_dice((6)))
            for pips, times in roll.items():
                results[pips] += times
        for times in results.values():
            assert times > 0

    @pytest.mark.parametrize('dice', [1, 2, 3, 4, 5, 6])
    def test_gl_roll_dice_pass_3(self, dice):
        """Test if the method returns tuple of the correct length"""
        assert len(GameLogic.roll_dice(dice)) == dice


class TestBanker:
    """Tests for the Banker class and its methods
    """
    @pytest.fixture()
    def banker(self):
        return Banker()

    def test_banker_instance(self):
        """Check class instantiation"""
        assert Banker()

    def test_banker_shelf_type_error(self, banker):
        with pytest.raises(TypeError) as err:
            assert banker.shelf('Points must be integer')
        assert str(err.value) == 'Points must be integer'

    def test_banker_self_pass_1(self, banker):
        """Test if the scores are added to the shelf"""
        banker.shelf(100)
        banker.shelf(50)
        assert banker.shelf_points == 150

    def test_banker_bank_pass_1(self, banker):
        """Test if the scores are added to the bank"""
        assert banker.shelf_points == 0
        assert banker.bank_points == 0
        banker.shelf(150)
        assert banker.shelf_points == 150
        assert banker.bank_points == 0
        assert banker.bank() == 150
        assert banker.shelf_points == 0
        assert banker.bank_points == 150

    def test_banker_clear_shelf_pass_1(self, banker):
        """Test if the scores are removed from the shelf"""
        assert banker.shelf_points == 0
        banker.shelf(200)
        assert banker.shelf_points == 200
        banker.clear_shelf()
        assert banker.shelf_points == 0
