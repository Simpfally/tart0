# pylint: skip-file
import unittest as u
from tarot.ai import *
from tarot.state import *

SEED = 22

# Bits copied from test_tarot_state.py


class test_determine_att(u.TestCase):
    def setUp(self):
        gen = random.Random()
        gen.seed(SEED)
        t3 = generate_random_playing_state(3, 0, gen)
        t4 = generate_random_playing_state(4, 0, gen)
        self.t3det = determine(t3.obs(), gen)
        self.t4det = determine(t4.obs(), gen)

    def test_size_of_decks(self):
        self.assertTrue(dog_size(self.t3det), "size of dog")
        self.assertTrue(cards_per_player(self.t3det, 3),
                        "deck size of player")

    def test_size_of_decks_four(self):
        self.assertTrue(cards_per_player(self.t4det, 4),
                        "deck size of player")
        self.assertTrue(dog_size(self.t4det), "size of dog")

    def test_all_card_used(self):
        self.assertTrue(all_cards(self.t3det),
                        "all cards are distributed")

    def test_all_card_used_four(self):
        self.assertTrue(all_cards(self.t4det),
                        "all cards are distributed")


class test_determine_def(u.TestCase):
    def setUp(self):
        gen = random.Random()
        gen.seed(SEED)
        t3 = generate_random_playing_state(3, 2, gen)
        t4 = generate_random_playing_state(4, 2, gen)
        self.t3det = determine(t3.obs(), gen)
        self.t4det = determine(t4.obs(), gen)

    def test_size_of_decks(self):
        self.assertTrue(dog_size(self.t3det), "size of dog")
        self.assertTrue(cards_per_player(self.t3det, 3),
                        "deck size of player")

    def test_size_of_decks_four(self):
        self.assertTrue(cards_per_player(self.t4det, 4),
                        "deck size of player")
        self.assertTrue(dog_size(self.t4det), "size of dog")

    def test_all_card_used(self):
        self.assertTrue(all_cards(self.t3det),
                        "all cards are distributed")

    def test_all_card_used_four(self):
        self.assertTrue(all_cards(self.t4det),
                        "all cards are distributed")


class test_determine_played(u.TestCase):
    def setUp(self):
        gen = random.Random()
        gen.seed(SEED)
        t3 = generate_random_playing_state(3, 2, gen)
        t3.step(t3.moves()[0])
        t3.step(t3.moves()[0])
        t3.step(t3.moves()[0])
        t3.step(t3.moves()[0])
        t4 = generate_random_playing_state(4, 2, gen)
        self.t3det = determine(t3.obs(), gen)
        self.t4det = determine(t4.obs(), gen)

    def test_size_of_decks(self):
        self.assertTrue(dog_size(self.t3det), "size of dog")

    def test_size_of_decks_four(self):
        self.assertTrue(dog_size(self.t4det), "size of dog")

    def test_all_card_used(self):
        self.assertTrue(all_cards(self.t3det),
                        "all cards are distributed")

    def test_all_card_used_four(self):
        self.assertTrue(all_cards(self.t4det),
                        "all cards are distributed")


def dog_size(state):
    return len(state.l_dog) == 6


def cards_per_player(state, N):
    b = True
    for i in range(0, N):
        b = b and len(state.ll_hand[i]) == 72//N
        if not b:
            print("player {} hand has {} cards when it should have had {}".format(
                i, len(state.ll_hand[i]), 72//N))
            return b
    return b


def all_cards(state):
    cards = {}
    for lcards in state.ll_hand:
        for c in lcards:
            cards[c] = 1

    for lcards in state.ll_pli:
        for c in lcards:
            cards[c] = 1

    for c in state.l_table:
        cards[c] = 1
    for c in state.l_dog:
        cards[c] = 1
    if len(cards) == 78:
        return True
    else:
        print("cards aren't all taken, {} missing : {}".format(
            78-len(cards), cards))

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
