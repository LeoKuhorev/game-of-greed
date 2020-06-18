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
        for _ in range(1000000):
            actual = GameLogic.roll_dice(1)
            assert 1 <= actual[0] <= 6

    def test_gl_roll_dice_pass_2(self):
        assert len(GameLogic.roll_dice(6)) == 6



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
        banker.shelf(100)
        banker.shelf(50)
        assert banker.shelf_points == 150

    def test_banker_bank_pass_1(self, banker):
        assert banker.shelf_points == 0
        assert banker.bank_points == 0
        banker.shelf(150)
        assert banker.shelf_points == 150
        assert banker.bank_points == 0
        assert banker.bank() == 150
        assert banker.shelf_points == 0
        assert banker.bank_points == 150

    def test_banker_clear_shelf_pass_1(self, banker):
        assert banker.shelf_points == 0 
        banker.shelf(200)
        assert banker.shelf_points == 200 
        banker.clear_shelf()
        assert banker.shelf_points == 0
