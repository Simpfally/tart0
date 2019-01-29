# pylint: skip-file
import unittest as u
from tarot.state import *
import random
import tarot.cards
import tarot.score

SEED = 22


class test_generate_random_playing_state(u.TestCase):
    def setUp(self):
        self.gen = random.Random()
        self.gen.seed(SEED)

    def test_size_of_decks(self):
        t = generate_random_playing_state(3, 0, self.gen)
        for i in range(0, 3):
            self.assertEqual(
                len(t.ll_hand[i]), 72//3, "deck size of player {}".format(i))
        self.assertEqual(len(t.l_dog), 6, "size of dog")

    def test_size_of_decks_four(self):
        t = generate_random_playing_state(4, 0, self.gen)
        for i in range(0, 4):
            self.assertEqual(
                len(t.ll_hand[i]), 72//4, "deck size of player {}".format(i))
        self.assertEqual(len(t.l_dog), 6, "size of dog")

    def test_all_card_used(self):
        t = generate_random_playing_state(3, 0, self.gen)
        cards = {}
        for lcards in t.ll_hand:
            for c in lcards:
                cards[c] = 1

        for c in t.l_dog:
            cards[c] = 1
        self.assertEqual(len(cards), 78, "all cards are distributed")

    def test_all_card_used_four(self):
        t = generate_random_playing_state(4, 0, self.gen)
        cards = {}
        for lcards in t.ll_hand:
            for c in lcards:
                cards[c] = 1

        for c in t.l_dog:
            cards[c] = 1
        self.assertEqual(len(cards), 78, "all cards are distributed")


# class test(u.TestCase):
#     def setUp(self):
#       pass
#
#     def tearDown(self):
#       pass
#     def test_funcc(self):
#         self.assertEqual(a,b, "msg")
# https://docs.python.org/3/library/unittest.html#module-unittest

if __name__ == '__main__':
    u.main()
