""" Flat Monte-Carlo players, c is the UCT constant """
from math import sqrt
import players.heuristics
from tarot.play import play_just
from tarot.cards import *


def fmc(N, gen):
    """ parameters that don't need to be registered """

    def fmc_f(params):
        """
        Parameterized class
        N : number  of player in the game
        n : amount of playout available
        n_d : amount of playout per determinisation
        cst_explo : constant of exploration to tune
        determine_deck : determiniser
        select_node : return the node to explore
        select_move : return the best move
        """

        class fmc_c:
            """ Flat Monte-Carlo tarot player """

            def __init__(self):
                self.n = params["n"]
                self.n_d = params["n_d"]
                self.cst_explo = params["cst_explo"]
                self.determine_deck = params["determine_deck"]
                self.gen = gen

                self.N_playout = 0
                self.t = None
                self.l_ai = [players.heuristics.random(
                    gen)() for _ in range(0, N)]

            def act(self, obs, movs):
                """ Return the move to play """
                self.t = None
                self.N_playout = 0
                self.determine(obs, movs)
                quota = self.n
                while quota > 0:
                    if quota % self.n_d == 0:
                        self.determine(obs, movs)
                    node = self.select_node()
                    node.playout()
                    self.N_playout += 1
                    quota -= 1
                return self.select_move()

            def determine(self, obs, movs):
                """ Update each node's state """
                obs_c = obs.copy()
                state = self.determine_deck(obs_c, self.gen)
                if self.t is None:
                    self.t = {}
                    for m in movs:
                        state_c = state.copy()
                        state_c.step(m)
                        self.t[m] = fmc_node(state_c, obs.n_toplay,
                                             self.cst_explo, self.gen, self.l_ai)
                else:
                    # update the state to the new determination
                    for m in self.t:
                        state_c = state.copy()
                        state_c.step(m)
                        self.t[m].state = state_c

            def select_move(self):
                """ Taken as an argument : must return which move to take """
                raise Exception("unimplemented")  # TODO

            def select_node(self):
                """ Taken as an argument : return which node to explore """
                raise Exception("unimplemented")  # TODO

        fmc_c.select_move = params["select_move"]
        fmc_c.select_node = params["select_node"]

        return fmc_c
    fmc_f.name = "Flat Monte Carlo"
    return fmc_f


class fmc_node:
    """ Node of a flat montecarlo, associated with a move """

    def __init__(self, state, n_track, cst_explo, gen, l_ai):
        self.cst_explo = cst_explo
        self.gen = gen
        # In the futur, could accept constructors
        self.l_ai = l_ai
        self.n_playout = 0
        self.n_won = 0
        self.wonpts = 0
        self.state = state
        self.n_track = n_track

    def uct(self, N_playout):
        """ Compute the uct value of the node """
        if self.n_playout == 0:
            return -1
        #exploi = self.n_won/self.n_playout
        exploi = self.wonpts/self.n_playout
        explor = sqrt(self.cst_explo*N_playout/self.n_playout)
        return exploi + explor

    def playout(self):
        """ Perform a playout from the intern state """
        state_c = self.state.copy()
        if not state_c.ended():
            play_just(state_c, self.l_ai, 0, 0)
        score = state_c.score()
        pts_won = score[self.n_track]
        self.wonpts += pts_won
        if pts_won > 0:
            self.n_won += 1
        self.n_playout += 1
