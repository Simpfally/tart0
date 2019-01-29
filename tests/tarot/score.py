# pylint: skip-file
import unittest as u
from tarot.score import *


class test_point_contrat(u.TestCase):
    def test_direct(self):
        self.assertEqual(point_contrat([1, 2, 3, 4, 24, 55, 66]), 56)
        self.assertEqual(point_contrat(
            [1, 2, 3, 4, 24, 55, 66, 14, 78]), 51)
        self.assertEqual(point_contrat(
            [1, 2, 3, 4, 24, 55, 66, 78, 50, 51, 57]), 41)
        self.assertEqual(point_contrat(
            [1, 2, 3, 77, 24, 55, 66, 78, 50, 51, 57]), 36)


class test_coef_enchere(u.TestCase):
    def test_direct(self):
        self.assertEqual(coef_enchere(0), 1)
        self.assertEqual(coef_enchere(1), 2)
        self.assertEqual(coef_enchere(2), 4)
        self.assertEqual(coef_enchere(3), 6)


class test_score_cards(u.TestCase):
    def setUp(self):
        self.allCards = [i for i in range(1, 79)]

    def test_all_cards(self):
        self.assertEqual(score_cards(self.allCards), 91)

    def test_all_but_1_cards(self):
        self.allCards.remove(1)
        self.assertEqual(score_cards(self.allCards), 90.5)

    def test_all_but_2_cards(self):
        self.allCards.remove(14)
        self.assertEqual(score_cards(self.allCards), 86.5)

    def test_all_but_3_cards(self):
        self.allCards.remove(77)
        self.assertEqual(score_cards(self.allCards), 86.5)

    def test_some_cards(self):
        self.assertEqual(score_cards([14, 28, 2]), 9.5)


class test_end_petit(u.TestCase):
    def setUp(self):
        pass

    @u.skip("waiting for tarot_state tests")
    def test_direct_useless(self):
        pass


# class test(u.TestCase):
#     def setUp(self):
#       pass
#
#     def tearDown(self):
#       pass


if __name__ == '__main__':
    u.main()
