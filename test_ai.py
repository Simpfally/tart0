""" Benchmark : a lot of random games in duplicate """
import argparse
import os.path
import sys
import random
import time
import types
from sys import argv
from tarot.state import *
from tarot.play import *
from tarot.cards import *
from tarot.ai import determine
import players.heuristics as heuristics
from players.fmc import fmc
from players.mc_select import *

def timedeltaform(t):
    days, r = divmod(int(t), 60*60*24)
    hours, r = divmod(r, 60*60)
    mins, secs = divmod(r, 60) 
    s = ""
    if days != 0:
        s += "{}d ".format(days)
    if hours!= 0:
        s += "{}h ".format(hours)
    if mins!= 0:
        s += "{}m ".format(mins)
    s += "{}s ".format(secs)

    return s.strip()

parser = argparse.ArgumentParser()
parser.add_argument("N", help="how many duplicaté", type=int)
parser.add_argument("-a", help="the parameter that varies")
parser.add_argument("-o", "--output", help="where to write experiment data")
args = parser.parse_args()
if args.output is None:
    print("Warning : scores won't be saved to a file since no filename has been given")
start_time = time.time()
gen = random.Random()
gen2 = random.Random()
gen.seed()
gen2.seed()

#seed = 46
#gen.seed(seed) # fix the donne
#gen2.seed(seed)

A = 400 #
if args.a is not None:
    A = int(args.a)

n = args.N
nb_players = 3
n_att = 0
n_playout = 500
n_play_per_deter = 1
c = 1000

ucb = fmc(nb_players, gen2)
params_A = { "N": nb_players,
        "n" : n_playout,
        "n_d": n_play_per_deter,
        "cst_explo": c,
        "determine_deck": determine,
        "select_node": node_uct,
        "select_move": move_wonpts
        }
params_A["n"] = 8
params_B = { "N": nb_players,
        "n" : n_playout,
        "n_d": n_play_per_deter,
        "cst_explo": c,
        "determine_deck": determine,
        "select_node": node_uct,
        "select_move": move_wonpts
        }

A_ai = ucb(params_A)
#B_ai = ucb(params_B)
B_ai = heuristics.random(gen2)
B_rand = True

if B_rand:
    print("PLayer B is a random player")

for x in params_A:
    a = params_A[x]
    b = params_B[x]
    if hasattr(a, '__call__'):
        a = params_A[x].__name__
        b = params_B[x].__name__
    if a == b or B_rand:
        print("{} \t<- {}".format(x, a))
    else:
        print("## A_ai.{} = {}\t B_ai.{} = {} ##".format(x, a, x, b))

############################
###### Experiment and results
############################
sfinal = [0,0]
scores = []
yfinal = 0
deg = False
deg = True
navg_l = [None]*30
for i in range(1, n+1):
    onetime = time.time()
    t = generate_random_playing_state(nb_players, n_att, gen)
    s, y = play_duplicate_oneONone(
        t, A_ai, B_ai, nb_players, 1, Verbose=0, Verify=0)
    score_de_A = s[0] - s[1]
    if args.output is not None:
        with open(args.output, "a") as f:
            f.write("{},{},".format(y, score_de_A))

    onetime = time.time() - onetime
    navg_l.pop(0)
    navg_l.append(onetime)
    ii = 0
    navg = 0
    coef = 1/30
    for x in navg_l:
        if x is not None:
            navg += x*coef
            ii += coef
            coef += 1/30
    navg = navg/ii

    scores.append(score_de_A)
    sfinal[0] += s[0]
    sfinal[1] += s[1]
    yfinal += y
    ta = time.time() - start_time
    s_dup = (ta/i*i/100 + navg*30/i)/(i/100 + 30/i)
    left = n-i
    timeleft = left*s_dup
    winpc = yfinal/i
    if deg:
        print("A_ai has {:.4f}% {:.2f}pts avg,\t {:.7f}s/duplicaté, {:.2f}s ({}) left (esti total {:.2f}s)".format(winpc, (sfinal[0] - sfinal[1])/i, s_dup, timeleft, timedeltaform(timeleft), s_dup*n))

t = time.time() - start_time
print(
    "{} done in {:.2f}s({}) so {:.2f}s/duplicate of {}players".format(n, t, timedeltaform(t), t/n, nb_players))
print("{:.2f}pts/game for A_ai, score of A_ai : {}, score of B_ai : {}".format(
    (sfinal[0] - sfinal[1])/n, sfinal[0]/n, sfinal[1]/n))
print("{:.2f} winrate for A_ai".format(yfinal/n))

#if args.output is not None:
#    text = ",".join([str(x) for x in scores])
#    filename = args.output
#    a = ""
#    if os.path.isfile(filename):
#        print("Overwrite {}? y/n".format(filename))
#        a = input()
#    if len(a) != 0 and a != 'n':
#        with open(filename, 'w') as f:
#            f.write(text)
#        print("Done, saved as {}".format(filename))
