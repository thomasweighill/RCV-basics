'''
Predict outcomes for minority groups under ranked choice voting
using four different models of voter behavior.

Enter basic input parameters under Global variables, then run the
code in order to simulate elections and output expected number of poc
candidates elected under each model and model choice.
'''


import numpy as np
from itertools import product, permutations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random, sys
import compute_winners as cw
from vote_transfers import cincinnati_transfer
from model_details import Cambridge_ballot_type, BABABA, luce_gaussian, luce_dirichlet, bradley_terry_dirichlet


### Global variables
poc_share = 0.30
poc_support_for_poc_candidates = 1.0-1e-5
poc_support_for_white_candidates = 1e-5
white_support_for_white_candidates = 1.0-1e-5
white_support_for_poc_candidates = 1e-5
num_ballots = 1000
num_simulations = 100
seats_open = 7
num_poc_candidates = 7
num_white_candidates = 7

print(sys.argv[0])
for s in [
    poc_share, poc_support_for_poc_candidates, poc_support_for_white_candidates,
    white_support_for_white_candidates, white_support_for_poc_candidates, num_ballots,
    num_simulations, seats_open, num_poc_candidates, num_white_candidates]:
    print(s)


### Luce model (Dirichlet variation)
concentrations = [0.5]*4 #>>1 means very similar supports, <<1 means most support goes to one or two candidates
#list goes [poc_for_poc, poc_for_white, white_for_poc, white_for_white]
concentration_list = [[0.5]*4, [2,0.5,0.5,0.5], [2,2,2,2], [2,2,0.5,0.5], [1.0]*4]


#simulate
poc_elected_luce_dirichlet = []
for i, concentrations in enumerate(concentration_list):
  print(concentrations)
  poc_elected_luce_dirichlet.append(luce_dirichlet(
      poc_share = poc_share,
      poc_support_for_poc_candidates = poc_support_for_poc_candidates,
      poc_support_for_white_candidates = poc_support_for_white_candidates,
      white_support_for_white_candidates = white_support_for_white_candidates,
      white_support_for_poc_candidates = white_support_for_poc_candidates,
      num_ballots = num_ballots,
      num_simulations = num_simulations,
      seats_open = seats_open,
      num_poc_candidates = num_poc_candidates,
      num_white_candidates = num_white_candidates,
      concentrations = concentrations
  ))
  print("\n")


print("Plackett-Luce Dirichelet predictions in order:")
for i, c in enumerate(concentration_list[:-1]):
  print(np.mean(poc_elected_luce_dirichlet[i]), "&", end=" ")
print(np.mean(poc_elected_luce_dirichlet[-1]))

### Bradley-Terry (Dirichlet variation)
concentrations = [0.5]*4 #>>1 means very similar supports, <<1 means most support goes to one or two candidates
#list goes [poc_for_poc, poc_for_white, white_for_poc, white_for_white]
concentration_list = [[0.5]*4, [2,0.5,0.5,0.5], [2,2,2,2], [2,2,0.5,0.5], [1.0]*4]


#simulate
poc_elected_bradley_terry_dirichlet = []
for i, concentrations in enumerate(concentration_list):
  print(concentrations)
  poc_elected_bradley_terry_dirichlet.append(bradley_terry_dirichlet(
      poc_share = poc_share,
      poc_support_for_poc_candidates = poc_support_for_poc_candidates,
      poc_support_for_white_candidates = poc_support_for_white_candidates,
      white_support_for_white_candidates = white_support_for_white_candidates,
      white_support_for_poc_candidates = white_support_for_poc_candidates,
      num_ballots = num_ballots,
      num_simulations = num_simulations,
      seats_open = seats_open,
      num_poc_candidates = num_poc_candidates,
      num_white_candidates = num_white_candidates,
      concentrations = concentrations
  ))
  print("\n")

print("Bradley-Terry Dirichelet predictions in order:")
for i, c in enumerate(concentration_list[:-1]):
  print(np.mean(poc_elected_bradley_terry_dirichlet[i]), "&", end=" ")
print(np.mean(poc_elected_bradley_terry_dirichlet[-1]))

### Alternating crossover model

#simulate
poc_elected_bababa = BABABA(
    poc_share = poc_share,
    poc_support_for_poc_candidates = poc_support_for_poc_candidates,
    poc_support_for_white_candidates = poc_support_for_white_candidates,
    white_support_for_white_candidates = white_support_for_white_candidates,
    white_support_for_poc_candidates = white_support_for_poc_candidates,
    num_ballots = num_ballots,
    num_simulations = num_simulations,
    seats_open = seats_open,
    num_poc_candidates = num_poc_candidates,
    num_white_candidates = num_white_candidates,
    scenarios_to_run = ['A', 'B', 'C', 'D'],
    verbose=False
)

print("Alternating crossover predictions in order:")
for i, c in enumerate(['A', 'B', 'C', 'D']):
  print(np.mean(poc_elected_bababa[c]), "&", end=" ")
print(np.mean([np.mean(poc_elected_bababa[c]) for c in ['A', 'B', 'C', 'D']]))

### Cambridge ballot types

#simulate
poc_elected_Cambridge = Cambridge_ballot_type(
    poc_share = poc_share,
    poc_support_for_poc_candidates = poc_support_for_poc_candidates,
    poc_support_for_white_candidates = poc_support_for_white_candidates,
    white_support_for_white_candidates = white_support_for_white_candidates,
    white_support_for_poc_candidates = white_support_for_poc_candidates,
    num_ballots = num_ballots,
    num_simulations = num_simulations,
    seats_open = seats_open,
    num_poc_candidates = num_poc_candidates,
    num_white_candidates = num_white_candidates,
    scenarios_to_run = ['A', 'B', 'C', 'D']
)

print("Cambridge sampler predictions in order:")
for i, c in enumerate(['A', 'B', 'C', 'D']):
  print(np.mean(poc_elected_Cambridge[c]), "&", end=" ")
print(np.mean([np.mean(poc_elected_Cambridge[c]) for c in ['A', 'B', 'C', 'D']]))
