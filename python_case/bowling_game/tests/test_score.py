import unittest
from lesson_014.bowling import Bowling


class BowlingTest(unittest.TestCase):

    def test_normal_game(self):
        self.bowling_test = Bowling('12X34-/1744XX23--')
        self.score = self.bowling_test.analyzing_result()
        self.assertEqual(self.score, 106)

    def test_only_strike_game(self):
        bowling_test = Bowling('XXXXXXXXXX')
        score = bowling_test.analyzing_result()
        self.assertEqual(score, 200)

    def test_only_loose_game(self):
        bowling_test = Bowling('--------------------')
        score = bowling_test.analyzing_result()
        self.assertEqual(score, 0)

    def test_lower_case(self):
        self.bowling_test = Bowling('xxxxxxxxxx')
        self.score = self.bowling_test.analyzing_result()
        self.assertEqual(self.score, 200)


if __name__ == '__main__':
    unittest.main()
