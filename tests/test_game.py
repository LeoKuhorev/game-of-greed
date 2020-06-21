import pytest

from game_of_greed.game import GameOfGreed
from game_of_greed.game_logic import GameLogic
from tests.flo.flo import Flo


class TestGame:

    @pytest.fixture()
    def game(self):
        return GameOfGreed()

    def mock_roll_dice(self, *args):
        return (1, 2, 3, 2, 3, 4)

    def test_wanna_play(self):
        Flo.test("tests/flo/wanna_play.txt")

    def test_do_wanna_play_then_quit(self):
        old_roll_dice = GameLogic.roll_dice
        GameLogic.roll_dice = self.mock_roll_dice

        Flo.test("tests/flo/do_wanna_play_then_quit.txt")

        GameLogic.roll_dice = old_roll_dice

    def test_cheat_and_fix(self):
        old_roll_dice = GameLogic.roll_dice
        GameLogic.roll_dice = self.mock_roll_dice

        Flo.test("tests/flo/cheat_and_fix.txt")

        GameLogic.roll_dice = old_roll_dice

    def test_bank_one_roll_then_quit(self):
        old_roll_dice = GameLogic.roll_dice
        GameLogic.roll_dice = self.mock_roll_dice

        Flo.test("tests/flo/bank_one_roll_then_quit.txt")

        GameLogic.roll_dice = old_roll_dice

    def test_bank_with_two_rounds(self):
        old_roll_dice = GameLogic.roll_dice
        GameLogic.roll_dice = self.mock_roll_dice

        Flo.test("tests/flo/bank_with_two_rounds.txt")

        GameLogic.roll_dice = old_roll_dice

    def test_example(self, capfd):
        """Another way to test STOUT
        """
        print("hello Tom")
        out, err = capfd.readouterr()
        assert out == "hello Tom\n"
