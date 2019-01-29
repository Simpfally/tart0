""" Benchmark : a lot of random games in duplicate """
import random
import players.heuristics as heuristics
from tarot.state import *
from tarot.play import *
from tarot.cards import *

n = 5000
seed = 28
N = 3
gen = random.Random()
gen.seed(seed)
t = generate_random_playing_state(N, 0, gen)
r_ai = heuristics.random(gen)

s, y = play_duplicate_oneONone(t, r_ai, r_ai, 3, n, False, False)

print((s[0] - s[1])/n, s[0]/n, s[1]/n)
print(y/n)
