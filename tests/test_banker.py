import pytest

from game_of_greed.banker import Banker


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
