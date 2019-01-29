""" Contains different variations of selecting a node and moves """


def node_uct(self):
    """ return the best node to explore based on uct """
    huct = -1000
    bn = None
    for m in self.t:
        u = self.t[m].uct(self.N_playout)
        if u == -1:
            return self.t[m]
        if u > huct:
            bn = self.t[m]
            huct = u
    return bn


def move_wonpts(self):
    """ return the best move to play """
    best = -1000
    bm = None
    for m in self.t:
        if self.t[m].n_playout == 0:
            continue
        u = self.t[m].wonpts/self.t[m].n_playout
        # print("{} : played {} times, {:.2f}% winrate, {:.2f} pts/game".format(pretty_hand(
        #    [m]), self.t[m].n_playout,
        # self.t[m].n_won/self.t[m].n_playout*100,
        # self.t[m].wonpts/self.t[m].n_playout))
        if u == -1:
            return m
        if u > best:
            bm = m
            best = u
    return bm
