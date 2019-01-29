""" Specify how experiments are stored and retrieved """
import pickle


class Experiment:
    """ Represent an experiment to be done """
# TODO add time spent

    def __init__(self, ft_ai, ft_params, sd_ai, sd_params):
        self.ft_ai = ft_ai
        self.ft_params = ft_params
        self.sd_ai = sd_ai
        self.sd_params = sd_params


class Element:
    """
    Represents an experiment, how many times it has been ran and its results
    """

    def __init__(self, ft_ai_name, ft_params, sd_ai_name, sd_params):
        self.ft_ai_name = ft_ai_name
        self.ft_params = ft_params
        self.sd_ai_name = sd_ai_name
        self.sd_params = sd_params

        self.n = 0
        self.ft_wins = 0
        self.ft_pts = 0
        self.sd_pts = 0


def pack_params(params):
    """ returns a tuple to be hashed, convert function into their name """
    lp = []
    for x in params:
        if callable(x):
            lp.append(x.__name__)
        else:
            lp.append(x)
    return tuple(lp)


def hash_params(exp):
    """ return the parameters' hash """
    return hash((exp.ft_ai.name, exp.sd_ai.name)) ^ hash(pack_params(exp.ft_params)) ^ hash(pack_params(exp.sd_params))
    # return (exp.ft_ai.name, exp.sd_ai.name) + pack_params(exp.ft_params) + pack_params(exp.sd_params)
    # return hash((exp.ft_ai.name, exp.sd_ai.name) +
    #            pack_params(exp.ft_params) + pack_params(exp.sd_params))


def register(db, exp, n, ft_wins, ft_pts, sd_pts):
    """ Register an experiment in the database """
    id_ex = hash_params(exp)
    # Reverse the order and it should contribute to the same thing
    id_ex_mirror = hash_params(Experiment(
        exp.sd_ai, exp.sd_params, exp.ft_ai, exp.ft_params))
    if not id_ex in db:
        db[id_ex] = Element(exp.ft_ai.name, exp.ft_params,
                            exp.sd_ai.name, exp.sd_params)
        db[id_ex_mirror] = Element(
            exp.ft_ai.name, exp.ft_params, exp.ft_ai.name, exp.ft_params)
    ex = db[id_ex]
    ex.n += n
    ex.ft_wins += ft_wins
    ex.ft_pts += ft_pts
    ex.sd_pts += sd_pts
    print("stored {} at hash {} and {}".format(ex.n, id_ex, id_ex_mirror))
    if id_ex != id_ex_mirror:
        ex_mir = db[id_ex_mirror]
        ex_mir.n += n
        ex_mir.ft_wins += n - ft_wins
        ex_mir.ft_pts += sd_pts
        ex_mir.sd_pts += ft_pts


def lookup(db, exp):
    """ return the element associated with the exp """
    id_ex = hash_params(exp)
    return db[id_ex]


def load_db(filename):
    """ return the loaded database """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def write_db(filename, db):
    """ Write the database to a file using pickle """
    with open(filename, 'wb') as f:
        pickle.dump(db, f, pickle.HIGHEST_PROTOCOL)
