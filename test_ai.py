""" Benchmark : a lot of random games in duplicate """
import random
import time
from sys import argv
from tarot.state import *
from tarot.play import *
from tarot.cards import *
from tarot.ai import determine
#import players.heuristics as heuristics
from players.fmc import fmc
from players.mc_select import *

start_time = time.time()
n = 1
if len(argv) > 1:
    n = int(argv[1])
# Seed 37 : 60% winrate for attacker, 28pts/game
N = 3
n_att = 0
gen = random.Random()
gen2 = random.Random()
gen.seed()
#gen.seed(seed) # fix the donne
#gen2.seed(seed)
gen2.seed()



n_playout = 400
n_play_per_deter = 1
c = 35
c2 = 9
seed = 46

ucb = fmc(N, gen2)
params_A = { "N": N,
        "n" : n_playout,
        "n_d": n_play_per_deter,
        "cst_explo": c,
        "determine_deck": determine,
        "select_node": node_uct,
        "select_move": move_wonpts
        }

params_B = { "N": N,
        "n" : n_playout,
        "n_d": n_play_per_deter*2,
        "cst_explo": c,
        "determine_deck": determine,
        "select_node": node_uct,
        "select_move": move_wonpts
        }
for x in params_A:
    #if params_A[x] != params_B[x]:
    print("A_ai.{} = {}\t B_ai.{} = {}".format(x, params_A[x], x, params_B[x]))
test = "r_ai.c = {} vs t_ai.c = {}".format(c2, c)
#print("Test ({} times) : {}".format(n, test))

#B_ai = heuristics.random(gen2)
A_ai = ucb(params_A)
B_ai = ucb(params_B)

#A_ai = fmc(N, n_playout, n_play_per_deter, c, node_uct, move_wonpts, determine, gen2)
#B_ai = fmc(N, n_playout, n_play_per_deter, c2,node_uct, move_wonpts, determine, gen2)
sfinal = [0,0]
yfinal = 0
deg = False
deg = True
for i in range(1, n+1):
    #gen = random.Random()
    #gen2 = random.Random()
    t = generate_random_playing_state(N, n_att, gen)
    s, y = play_duplicate_oneONone(
        t, A_ai, B_ai, N, 1, Verbose=0, Verify=1)
    sfinal[0] += s[0]
    sfinal[1] += s[1]
    yfinal += y
    ta = time.time() - start_time
    s_dup = ta/i
    left = n-i
    timeleft = left*s_dup
    if deg:
        print("A_ai has {:.2f}pts avg,\t {:.2f}s/duplicaté, {:.2f}s left".format((sfinal[0] - sfinal[1])/i, ta/i, timeleft))


t = time.time() - start_time
print(
    "{} done in {:.2f}s so {:.2f}s/duplicate of {}players".format(n, t, t/n, N))
print("{:.2f}pts/game for A_ai, score of A_ai : {}, score of B_ai : {}".format(
    (sfinal[0] - sfinal[1])/n, sfinal[0]/n, sfinal[1]/n))
print("{:.2f} winrate for A_ai".format(yfinal/n))
