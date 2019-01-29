""" Helper functions to use the database of experiments """
from experiments import store
from tarot.play import play_duplicate_oneONone


def single_test(t, ft_ai, ft_params, sd_ai, sd_params, N, n, db=None, filename="", Verbose=1):
    """ do it all function """
    ft_i = ft_ai(ft_params)
    sd_i = sd_ai(sd_params)
    exp = store.Experiment(ft_ai, ft_params, sd_ai, sd_params)

    sc, ft_wins = play_duplicate_oneONone(t, ft_i, sd_i, N, n)
    # TODO maybe not use play_duplicate, redo it here
    # to be able to show real time progress, duplicate/s
    ft_pts, sd_pts = sc[0], sc[1]

    if db is None and filename != "":
        try:
            db = store.load_db(filename)
        except FileNotFoundError:
            db = {}

    if not db is None:
        store.register(db, exp, n, ft_wins, ft_pts, sd_pts)
        if filename != "":
            store.write_db(filename, db)
        el = store.lookup(db, exp)
        ft_wins = el.ft_wins
        ft_pts = el.ft_pts
        sd_pts = el.sd_pts
        n = el.n
    if Verbose:
        ft_l = []
        for k in ft_params:
            v = ft_params[k]
            if callable(v):
                v = v.__name__
            ft_l.append("{} : {}".format(k, v))
        ft_s = " ; ".join(ft_l)
        sd_l = []
        for k in sd_params:
            v = sd_params[k]
            if callable(v):
                v = v.__name__
            sd_l.append("{} : {}".format(k, v))
        sd_s = " ; ".join(sd_l)
        print("{} Tests\nFst : {}\nSnd: {}".format(n, ft_s, sd_s))
        print("{:.2f}% win rate ({} wins) with {:.2f}pts/dupli and {:.2f}pts/d".format(
            ft_wins/n*100, ft_wins, ft_pts/n, sd_pts/n))
