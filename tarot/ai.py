""" General functions for tarot ai """
import random
from tarot.state import *
from tarot.cards import ecartable


def determine(obs, gen=None):
    """
    Takes an observation of a state and produce a randomized state
    Modify the observation (by appending list etc)
    """
    if gen is None:
        gen = random.Random()

    free = [1]*79
    free[0] = 0

    for c in obs.ll_hand[obs.n_toplay]:
        free[c] = 0
    for lc in obs.ll_pli:
        for c in lc:
            assert free[c] == 1, "pli"
            free[c] = 0
    for c in obs.l_table:
        assert free[c] == 1, "table"
        free[c] = 0

    # empty if it shouldn't be seen anyway
    for c in obs.l_dog:
        free[c] = 0

    card_per_player = []
    for i in range(0, obs.N):
        if i == obs.n_toplay:
            # we known all of our cards
            card_per_player.append(0)
        else:
            # see tarot_state / determine : hand size is given in obs
            card_per_player.append(obs.ll_hand[i][0])
            obs.ll_hand[i] = []
   # print(obs.n_att, obs.n_toplay, card_per_player, 6-len(obs.l_dog),
   #       len([i for i in free if i]))

    # Distribute cards from seen dog equally between
    # Attacker and dog
    if len(obs.l_dog) < 6:
        for c in obs.l_seen_dog:
            if not free[c]:
                continue
            i = gen.randint(0, 1)
            if i == 1 and card_per_player[obs.n_att] > 0:
                card_per_player[obs.n_att] -= 1
                obs.ll_hand[obs.n_att].append(c)
            else:
                obs.l_dog.append(c)
            free[c] = 0
    for c in range(1, 79):
        #    print(obs.n_att, obs.n_toplay, card_per_player, 6-len(obs.l_dog),
        #          len([i for i in free if i]))
        if not free[c]:
            continue
        to_fill = []
        for i in range(0, obs.N):
            if card_per_player[i] > 0:
                to_fill.append((obs.ll_hand[i], i))
        n_hand = len(to_fill) - 1
        if len(obs.l_dog) < 6 and ecartable(c):
            to_fill.append(obs.l_dog)
        if not to_fill:
            return obs
        j = gen.randint(0, len(to_fill)-1)
        # TODO cleanup this shit
        if j <= n_hand:
            card_per_player[to_fill[j][1]] -= 1
            to_fill[j][0].append(c)
        else:
            to_fill[j].append(c)
        free[c] = 0
    l1 = len(obs.ll_hand[0])
    l2 = len(obs.ll_hand[1])
    l3 = len(obs.ll_hand[2])
    if abs(l1 - l2) > 1 or abs(l1 - l3) > 1 or abs(l3 - l2) > 1:
        # TODO cleanup
        # print(l1, l2, l3)
        # print(o)
        # print("lendog", len(obs.l_dog))
        # print("had to place {} cards".format(CARD_TO_PLACE))
        assert False, "non"

    return obs
