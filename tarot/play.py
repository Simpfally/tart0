"""
Helper functions to play a game between players.
Unless otherwise specified, functions will affect the given state
so that multiple games on the same state require using state.copy()
"""
import random
import players.heuristics as heuristics
from tarot.cards import pretty_hand


def play_just(state, l_players, Verbose=0, Verify=False):
    """
    Most lightweight play function, accept player instance
    Do not return anything, check score with state.score()
    """
    assert not state.ended(), "The state to be played has already come to an end."

    playing = True
    if Verbose:
        for i in range(0, state.N):
            if i == state.n_att:
                print("{} is {}, an Attacker".format(
                    i, l_players[i].name))
            else:
                print("{} is {}, a defender".format(i, l_players[i].name))
            print(pretty_hand(state.ll_hand[i]))
    while playing:
        if Verbose == 2:
            print("------------------------------")
        # compute the moves of n_toplay and store them in s_moves
        m = state.moves()
        if Verify:
            if not m:
                print(state.ll_hand[0])
                print(state.ll_hand[1])
                print(state.ll_hand[2])
                print(len(state.ll_all_pli))
                assert False
        if Verbose == 2:
            print(state.n_toplay, "is playing")
            print(pretty_hand(state.ll_hand[state.n_toplay]))

        a = l_players[state.n_toplay].act(state.obs(), m)
        playing = state.step(a, Verbose, Verify)


def play_simple(state, l_c_players, Verbose=0, Verify=False):
    """ Still lightweight, takes the constructors of players """
    l_players = []
    for g_ply in l_c_players:
        l_players.append(g_ply())
    play_just(state, l_players, Verbose, Verify)


def play_duplicate(state, l_playersA, l_playersB, Verbose=0, Verify=False):
    """
    Given two list(teams) of equal length of players, return the score of
    both teams computed from two match played on the same state.
    The first player of each team will be the attacker.
    Only do two games, do not change the given state
    n_att must be 1
    """
    state_c = state.copy()

    # Form the two list players
    players_1 = [l_playersA[0]]
    players_2 = [l_playersB[0]]
    for p in l_playersB[1:]:
        players_1.append(p)
    for p in l_playersA[1:]:
        players_2.append(p)

    # Get the scores of the two games
    play_just(state_c, players_1, Verbose, Verify)
    score_1 = state_c.score(Verbose=Verbose)
    state_c = state.copy()
    play_just(state_c, players_2, Verbose, Verify)
    score_2 = state_c.score(Verbose=Verbose)

    score_A = score_1[0]
    score_B = score_2[0]
    if Verbose:
        print("Team A's attacker won {}pts".format(score_A))
        print("Team B's attacker won {}pts".format(score_B))
    for s in score_1[1:]:
        if Verbose:
            print("B defender score : {}".format(s))
        score_B += s
    for s in score_2[1:]:
        if Verbose:
            print("A defender score : {}".format(s))
        score_A += s
    return score_A, score_B


def play_duplicate_oneONone(state, plyA, plyB, N, n, Verbose=0, Verify=False):
    """
    Given two constructors, play n duplicates
    return the score of both teams and the amount of win of team A
    """
    l_playersA = [plyA() for _ in range(0, N)]
    l_playersB = [plyB() for _ in range(0, N)]
    s = (0, 0)
    wA = 0
    for _ in range(0, n):
        a = play_duplicate(state, l_playersA, l_playersB, Verbose, Verify)
        if a[0] > a[1]:
            wA += 1
        s = (s[0]+a[0], s[1]+a[1])
    return s, wA


def evaluate_deck(state, n, gen=None, Verbose=0):
    """
    Given a state, run random plays to determine if it's biased for any
    player
    """
    if gen is None:
        gen = random.Random()
        gen.seed()
    s = [0] * state.N
    wins_att = 0
    l_players = [heuristics.random(gen)() for _ in range(0, state.N)]
    for _ in range(0, n):
        state_c = state.copy()
        play_just(state_c, l_players, Verbose=Verbose)
        y = state_c.score()
        if y[state.n_att] > 0:
            wins_att += 1
        addlist(s, y)

    return [i/n for i in s], wins_att


def addlist(a, b):
    """ add two list element wise """
    for x, y in enumerate(b):
        a[x] += y
