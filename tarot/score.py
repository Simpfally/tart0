""" Include functions about computing the score of cards """
from tarot.cards import *


def point_contrat(l_cards):
    """ Return the amounts of points needed by the attacker """
    s = 0
    for c in l_cards:
        if c == PETIT or c == TWENTY or c == EXCUSE:
            s += 1
    if s > 3:
        print(pretty_hand(l_cards))
        return 0
    points = [56, 51, 41, 36]

    return points[s]


def coef_enchere(enchere):
    """ Renvoie le coefficient correspondant à l'enchere prise """
    return max(2*enchere, 1)


def score_cards(l_cards):
    """ Renvoie le nombre de points correspondants à ces cartes """
    s = 0
    for i in l_cards:
        c, v = card_info(i)
        if c == 0:
            if v == 1 or v == 21:
                s += 4.5
            else:
                s += 0.5
        elif c == -1:
            s += 4.5
        elif v <= 10:
            s += 0.5
        else:
            s += 0.5 + (v-10)
    return s


def end_petit(ll_all_pli, N, n_att):
    """
    Si l'attaque prend le petit au dernier pli, on renvoie 1, -1 si c'est la défense et 0 sinon
    """
    last_pli = 72//N - 1
    if PETIT in ll_all_pli[last_pli][0]:
        if ll_all_pli[last_pli][1] == n_att:
            return 1
        return -1
    return 0
