""" Contain basic heuristic or random AI for tarot """


def random(gen):
    """ Parameterized class """
    class random_c:
        """
        Simply return a random move among the possible
        ones
        """
        name = "tarot_random_ai"

        def __init__(self):
            self.gen = gen

        def act(self, obs, moves):
            # pylint: disable=unused-argument
            """ Return the move to play """
            return self.gen.choice(moves)
    return random_c


def heuristic(gen):
    """ Parameterized class """
    class heuristic_c:
        """
        62% winrate vs random
        """
        name = "tarot_heuristic"

        def __init__(self):
            self.gen = gen

        def act(self, obs, moves):
            """ Return the move to play """
            if obs.n_decidante == obs.n_att:
                return moves[0]
            return self.gen.choice(moves)
    return heuristic_c
