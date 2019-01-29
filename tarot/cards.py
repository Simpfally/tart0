""" Fonctions utiles pour les cartes """

PETIT = 57
TWENTY = 77
EXCUSE = 78


def ecartable(c):
    """ Return true if the card can be placed in the dog """
    if c == PETIT or c == TWENTY or c == EXCUSE:
        return False
    if c <= 56 and c % 14 == 0:
        return False
    return True


def decidante(old, new):
    """
    Calcul la nouvelle carte décidante
    renvoie un couple : Booléen si la carte a changé
    et la nouvelle carte décidante
    """
    if old == 0:
        return True, new
    o_col, o_val = card_info(old)
    n_col, n_val = card_info(new)

    # l'excuse ne change pas la carte décidante de toute façon
    if o_col == -1:
        return True, new
    if n_col == 0:
        if (o_col == 0 and n_val < o_val):
            return False, old
        return True, new
    elif n_col > 0:
        if n_col == o_col:
            if n_val > o_val:
                return True, new
    return False, old


def card_info(i):
    """
    renvoie la couleur et la valeur d'une carte
    couleur | signification | valeur
    -1      | L'excuse      | 0
    0       | Un atout      | 1...21
    1,2,3,4 | Une couleur   | 1...14
    """
    assert i > 0 and i <= 78, "numéro de carte invalide"
    if i == EXCUSE:  # L'excuse
        return -1, 0
    if i > 56:
        return 0, i - 56
    i -= 1
    col = i//14 + 1
    val = i % 14 + 1
    return col, val


def info_card(col, val):
    """ renvoie le numéro de carte à partir d'une couleur et valeur """
    assert col in [-1, 0, 1, 2, 3, 4], "invalid color"
    if col == -1:
        return EXCUSE
    if col == 0:
        assert val >= 1 and val <= 21
        return 56 + val
    assert val >= 1 and val <= 14
    return (col - 1)*14 + val


PCARD = {
    1: "♠1",
    2: "♠2",
    3: "♠3",
    4: "♠4",
    5: "♠5",
    6: "♠6",
    7: "♠7",
    8: "♠8",
    9: "♠9",
    10: "♠10",
    11: "♠V",
    12: "♠C",
    13: "♠Q",
    14: "♠K",
    15: "♥1",
    16: "♥2",
    17: "♥3",
    18: "♥4",
    19: "♥5",
    20: "♥6",
    21: "♥7",
    22: "♥8",
    23: "♥9",
    24: "♥10",
    25: "♥V",
    26: "♥C",
    27: "♥Q",
    28: "♥K",
    29: "♦1",
    30: "♦2",
    31: "♦3",
    32: "♦4",
    33: "♦5",
    34: "♦6",
    35: "♦7",
    36: "♦8",
    37: "♦9",
    38: "♦10",
    39: "♦V",
    40: "♦C",
    41: "♦Q",
    42: "♦K",
    43: "♣1",
    44: "♣2",
    45: "♣3",
    46: "♣4",
    47: "♣5",
    48: "♣6",
    49: "♣7",
    50: "♣8",
    51: "♣9",
    52: "♣10",
    53: "♣V",
    54: "♣C",
    55: "♣Q",
    56: "♣K",
    57: "T1",
    58: "T2",
    59: "T3",
    60: "T4",
    61: "T5",
    62: "T6",
    63: "T7",
    64: "T8",
    65: "T9",
    66: "T10",
    67: "T11",
    68: "T12",
    69: "T13",
    70: "T14",
    71: "T15",
    72: "T16",
    73: "T17",
    74: "T18",
    75: "T19",
    76: "T20",
    77: "T21",
    78: "JJ"
}


def pretty_cards(l_cards, brack=True):
    """ return the formatted list of cards """
    if not l_cards:
        if brack:
            return "[]"
        return ""
    # Si c'est sous forme d'un tableau de 78
    s = None
    if brack:
        s = "[{}]"
    else:
        s = "{}"
    return s.format(', '.join([PCARD[c] for c in l_cards]))


def pretty_hand(l_cards):
    """ return pretty cards sorted by color, in color """
    s = [[] for i in range(0, 5)]
    for i in l_cards:
        c, v = card_info(i)
        if c == -1:
            c = 0
        s[c].append(pretty_cards([i], False))
    ss = []
    i = 1
    for v in s:
        if v:
            vv = ", ".join(v)
            vvv = "\x1b[0;3{};40m{}\x1b[0m".format(i, vv)
            ss.append(vvv)
        i += 1

    return " // ".join(ss)
