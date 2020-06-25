import pytest

from game_of_greed.game import GameOfGreed
from game_of_greed.game_logic import GameLogic
from tests.flo.flo import Flo


class TestGame:

    @pytest.fixture()
    def game(self):
        return GameOfGreed()


    def test_wanna_play(self):
        Flo.test("tests/flo/wanna_play.txt")

    def test_do_wanna_play_then_quit(self):
        Flo.test("tests/flo/do_wanna_play_then_quit.txt")

    def test_cheat_and_fix(self):
        Flo.test("tests/flo/cheat_and_fix.txt")

    def test_bank_one_roll_then_quit(self):
        Flo.test("tests/flo/bank_one_roll_then_quit.txt")

    def test_bank_first_for_two_rounds(self):
        Flo.test("tests/flo/bank_first_for_two_rounds.txt")

    def test_hot_dice(self):
        Flo.test("tests/flo/hot_dice.txt")

    def test_living_on_the_edge(self):
        Flo.test("tests/flo/living_on_the_edge.txt")

    def test_quitter(self):
        Flo.test("tests/flo/quitter.txt")
        
    def test_zilch(self):
        Flo.test("tests/flo/zilch.txt")


    # def test_example(self, capfd):
    #     """Another way to test STOUT
    #     """
    #     print("hello Tom")
    #     out, err = capfd.readouterr()
    #     assert out == "hello Tom\n"
