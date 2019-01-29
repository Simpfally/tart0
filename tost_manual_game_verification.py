""" forgot how to disable pylint """
import random
from tarot.cards import *
from tarot.state import *
from tarot.score import *


gen = random.Random()
gen.seed(22)

n = 3
t = generate_random_playing_state(n, 0, gen)

for i in range(0, n):
    print(i, pretty_hand(t.ll_hand[i]))
print("Next to play :", t.n_toplay)
print(pretty_hand(t.s_moves))

def showtour(tt):
    tt.moves()
    print("table :", pretty_hand(tt.l_table))
    print("moves : ", pretty_hand(tt.s_moves))
    print("moves : ", tt.s_moves)


showtour(t)
t.step(32, Verbose=True)
showtour(t)
t.step(78, Verbose=True)
showtour(t)
t.step(39, Verbose=True)
showtour(t)


for i in range(0, n):
    print("{}'s pli:{}".format(i, pretty_hand(t.ll_pli[i])))
for i in range(0, n):
    print("{}'s score: {}pts".format(i, score_cards(t.ll_pli[i])))

#assert score_cards(
#    t.ll_pli[0]) == 16, "the score changed for one player it seems"
# last time ran, the last 6 lines are :
# 0's pli:JJ, T19, T1 // ♣10, ♣9, ♣V, ♣C, ♣1, ♣7, ♣5
# 1's pli:T14, T21, T6 // ♣K, ♣Q
# 2's pli:T9, T10, T15
# 0's score: 16.0pts
# 1's score: 13.5pts
# 2's score: 1.5pts
