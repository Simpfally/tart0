# pylint: skip-file
import unittest as u
from tarot.cards import *


class test_decidante(u.TestCase):
    def test_direct(self):
        test_params = [
            (1, 2),
            (13, 9),
            (2, 15),
            (78, 29),
            (77, 75),
            (57, 13),
            (12, 58)]
        test_answers = [
            (1, 2),
            (0, 13),
            (0, 2),
            (1, 29),
            (0, 77),
            (0, 57),
            (1, 58)]
        for x, y in zip(test_params, test_answers):
            a, b = decidante(*x)
            self.assertEqual(a, y[0], "{} -> {}".format(*x))
            self.assertEqual(b, y[1], "{} -> {}".format(*x))


class test_card(u.TestCase):
    def setUp(self):
        self.test_cards = [1, 14, 28, 56, 57, 77, 78]
        self.test_info = [(1, 1), (1, 14), (2, 14),
                          (4, 14), (0, 1), (0, 21), (-1, 0)]

    def test_card_info(self):
        for x, y in zip(self.test_cards, self.test_info):
            a, b = card_info(x)
            self.assertEqual(a, y[0], "{}".format(x))
            self.assertEqual(b, y[1], "{}".format(x))

    def test_info_card(self):
        for x, y in zip(self.test_info, self.test_cards):
            a = info_card(x[0], x[1])
            self.assertEqual(a, y, "{}".format(x))

# class test(u.TestCase):
#     def setUp(self):
#       pass
#
#     def tearDown(self):
#       pass


if __name__ == '__main__':
    u.main()
