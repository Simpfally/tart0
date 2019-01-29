""" Class and functions around the state of the game """

import random
from tarot.cards import *
from tarot.score import *


class State:
    """ Define the state of the Tarot game """

    def __init__(self):
        self.enchere = 0
        self.stade = 0

        self.ll_hand = None
        self.ll_pli = None
        self.l_table = None
        self.l_dog = None
        self.l_seen_dog = None
        self.l_used = None

        self.N = 0
        self.n_att = 0
        self.n_decidante = 0
        self.c_decidante = 0
        self.n_toplay = 0

        # Tells which player needs/owes a low card because of the excuse
        self.n_owed_low = -1
        self.n_owe_low = -1

        # chaque pli contient (pli, n_decidante) pour ce tour
        self.ll_all_pli = None

        self.s_moves = []

    def copy(self):
        """ Return a deep copy of itself """
        t = State()

        t.enchere = self.enchere
        t.stade = self.stade

        t.ll_hand = []
        t.ll_pli = []
        for i in range(0, self.N):
            t.ll_hand.append(self.ll_hand[i].copy())
            t.ll_pli.append(self.ll_pli[i].copy())
        t.l_table = self.l_table.copy()
        t.l_dog = self.l_dog.copy()
        t.l_seen_dog = self.l_seen_dog.copy()
        t.l_used = self.l_used.copy()

        t.N = self.N
        t.n_att = self.n_att
        t.n_decidante = self.n_decidante
        t.c_decidante = self.c_decidante
        t.n_toplay = self.n_toplay

        t.ll_all_pli = []
        for i in range(0, len(self.ll_all_pli)):
            t.ll_all_pli.append(self.ll_all_pli[i])

        return t

    def obs(self, n_j=-1):
        """
        Return an observation(modified state) (according to rules
        of the state) of the given player (or n_toplay by default)
        Hands of other players only include one integer : how many cards they have
        """

        if n_j == -1:
            n_j = self.n_toplay

        t = State()
        t.l_seen_dog = []
        t.l_dog = []
        # Dans le cas d'une prise ou d'une garde
        if self.enchere < 2:
            t.l_seen_dog = self.l_seen_dog
            # L'attaquant peut voir son chien
            if n_j == self.n_att:
                t.l_dog = self.l_dog

        t.ll_hand = []
        t.ll_pli = []

        # Le joueur ne voit que sa main
        for i in range(0, self.N):
            if i == n_j:
                t.ll_hand.append(self.ll_hand[i])
            else:
                t.ll_hand.append([len(self.ll_hand[i])])
            t.ll_pli.append(self.ll_pli[i])

        t.enchere = self.enchere
        t.stade = self.stade

        t.l_table = self.l_table
        t.l_used = self.l_used

        t.N = self.N
        t.n_att = self.n_att
        t.n_decidante = self.n_decidante
        t.c_decidante = self.c_decidante
        t.n_toplay = self.n_toplay

        t.ll_all_pli = self.ll_all_pli
        return t

    def step(self, card, Verbose=0, Verif=False):
        """
        Modify the state by playing a card for n_toplay
        step uses s_moves for verification
        Return 1 iff the game is still going
        """
        # TODO add the choose dog step
        n = self.n_toplay
        if Verif:
            assert card in self.s_moves, "Player {} tried to play {} which he cannot".format(
                n, card)

        if Verbose:
            name = "Defender"
            if n == self.n_att:
                name = "Attacker"
            print("{}({}) played {}({})".format(
                name, n, pretty_hand([card]), card))

        changed, self.c_decidante = decidante(self.c_decidante, card)
        if changed:
            self.n_decidante = n

        if card == EXCUSE:
            self.n_owe_low = n

        self.ll_hand[n].remove(card)
        self.l_table.append(card)

        self.n_toplay = (self.n_toplay + 1) % self.N
        if len(self.l_table) == self.N:
            self.end_pli(Verbose)

        if self.ended():
            return False

        return True

    def end_pli(self, Verbose=False):
        """ Simple factoring of what happens when a pli is completed """
        if Verbose == 2:
            for i in range(0, self.N):
                print(i, pretty_hand(self.ll_hand[i]))
        n = self.n_decidante
        self.ll_all_pli.append((self.l_table.copy(), n))
        if EXCUSE in self.l_table:
            self.n_owed_low = n
            self.l_table.remove(EXCUSE)
            self.ll_pli[self.n_owe_low].append(EXCUSE)
        self.ll_pli[n].extend(self.l_table)
        if Verbose:
            name = "Defender"
            pts = score_cards(self.ll_pli[n])
            if n == self.n_att:
                name = "Attacker"
                pts += score_cards(self.l_dog)
            print("Pli n°{} : {}({}) won {} and now has {}pts".format(
                len(self.ll_all_pli), name, n, pretty_hand(self.l_table), pts))
            print("----------------------")
        self.l_table = []
        self.n_toplay = self.n_decidante
        self.c_decidante = 0
        self.n_decidante = 0

    def moves(self, n_j=-1):
        """ saves the moves to the state for futur use and return it """
        m = self.moves_a(n_j)
        self.s_moves = m
        return m

    def moves_a(self, n_j):
        """ return a list of all possible movements for the player """
        if n_j == -1:
            n_j = self.n_toplay

        m = self.ll_hand[n_j]

        if self.c_decidante == 0:
            return m
        d_col, d_val = card_info(self.c_decidante)
        if d_col == -1:
            return m

        atout = []
        good_col = []
        excuse = 0
        for card in m:
            c, v = card_info(card)
            if c == -1:
                excuse = 1
            elif c == 0:
                atout.append(card)
            elif c == d_col:
                good_col.append(card)

        if d_col > 0:
            if good_col:
                return add_excuse(excuse, good_col)
            if not atout:
                return m
            return add_excuse(excuse, atout)
        else:
            if not atout:
                return m
            atout_sup = []
            for card in atout:
                c, v = card_info(card)
                if v > d_val:
                    atout_sup.append(card)
            if not atout_sup:
                return add_excuse(excuse, atout)
            return add_excuse(excuse, atout_sup)

    def ended(self):
        """ Return true if all pli are done """
        return len(self.ll_all_pli) == 72//self.N

    def score(self, Verbose=0):
        """ Return a list of the score of each players """
        score_att = 0
        # The dog is only counted at the end
        if self.ended():
            if self.enchere < 2:
                score_att += score_cards(self.l_dog)
            elif self.enchere == 4:
                score_att -= score_cards(self.l_dog)
        score_att += score_cards(self.ll_pli[self.n_att])

        # Those lines will play in some cases
        if self.n_owe_low == self.n_att:
            score_att -= 0.5
        elif self.n_owed_low == self.n_att:
            score_att += 0.5

        diff = score_att - point_contrat(self.ll_pli[self.n_att])

        score = diff
        if Verbose:
            print("The Attacker won {}pts ({} hand + {} dog)".format(
                score_att, score_cards(self.ll_pli[self.n_att]),
                score_cards(self.l_dog)))
        # If the attacker won the contract
        if diff > 0:
            score += 25
            if Verbose:
                print("His contract was {}pts so he won".format(
                    point_contrat(self.ll_pli[self.n_att])))
        else:
            if Verbose:
                print("His contract was {}pts so he lost".format(
                    point_contrat(self.ll_pli[self.n_att])))
            score -= 25

        score += 10*end_petit(self.ll_all_pli, self.N, self.n_att)

        score *= coef_enchere(self.enchere)

        s_att = score * self.N
        scores = []

        # TODO normalement dans l'ordre
        for i in range(0, self.N):
            if i == self.n_att:
                scores.append(s_att)
            else:
                scores.append(-score)

        return scores

    def score_simple(self):
        """ Return a list of the score of each players' cards """
        score_att = 0
        # The dog is only counted at the end
        if self.ended():
            if self.enchere < 2:
                score_att += score_cards(self.l_dog)
            elif self.enchere == 4:
                score_att -= score_cards(self.l_dog)
        score_att += score_cards(self.ll_pli[self.n_att])

        scores = []

        # TODO normalement dans l'ordre
        for i in range(0, self.N):
            if i == self.n_att:
                scores.append(score_att)
            else:
                scores.append(score_cards(self.ll_pli[i]))

            if self.n_owe_low == i:
                scores[i] -= 0.5
            elif self.n_owed_low == i:
                scores[i] += 0.5

        return scores


def generate_blank_state(N):
    """ Return a fresh state with everything allocated """
    state = State()

    state.N = N

    state.ll_hand = []
    state.ll_pli = []
    state.l_table = []
    state.l_dog = []
    state.l_seen_dog = []
    state.l_used = []

    for _ in range(0, state.N):
        state.ll_hand.append([])
        state.ll_pli.append([])

    state.ll_all_pli = []

    return state


def generate_random_playing_state(N, n_att=0, generator=None):
    """
    Return a fresh state that is ready to play :
    stade = 2, enchere = 0 (prise)
    dog is given
    """

    if generator is None:
        generator = random.Random()
    state = generate_blank_state(N)
    state.n_att = n_att

    cartes = list(range(1, 79))
    generator.shuffle(cartes)
    ki = len(cartes) - 1
    for _ in range(0, 6):
        state.l_seen_dog.append(cartes[ki])
        i = generator.randint(0, 1)
        if i:
            state.l_dog.append(cartes[ki])
        else:
            state.ll_hand[n_att].append(cartes[ki])
        ki -= 1
    while ki > 0:
        if len(state.l_dog) < 6:
            state.l_dog.append(cartes[ki])
            ki -= 1
        for i in range(0, state.N):
            if len(state.ll_hand[i]) < 72//state.N:
                state.ll_hand[i].append(cartes[ki])
                ki -= 1

    return state


def add_excuse(excuse, m):
    """ helper function : add the excuse card if needed """
    if excuse:
        m.append(EXCUSE)
    return m
