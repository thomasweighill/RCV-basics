import pickle
from numpy.random import choice
from collections import defaultdict
import compute_winners as cw
import numpy as np
from itertools import permutations, product
import random
from vote_transfers import cincinnati_transfer

def Cambridge_ballot_type(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    scenarios_to_run = ['A', 'B', 'C', 'D']
):

    num_candidates = [num_poc_candidates, num_white_candidates]
    minority_share = poc_share
    preference_strengths = [white_support_for_white_candidates, poc_support_for_poc_candidates]
    num_seats = seats_open
    poc_elected_Cambridge = defaultdict(list)
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]

    white_candidates = candidates[num_candidates[0]:]
    poc_candidates = candidates[:num_candidates[0]]

    #get ballot type frequencies
    ballot_type_frequencies = pickle.load(open('Cambridge_09to17_ballot_types.p', 'rb'))
    white_first_probs = {x:p for x,p in ballot_type_frequencies.items() if x[0]=='W'}
    poc_first_probs = {x:p for x,p in ballot_type_frequencies.items() if x[0]=='C'}
    sum_white_first_probs = sum(white_first_probs.values())
    white_first_probs = {x:p/sum_white_first_probs for x,p in white_first_probs.items()}
    sum_poc_first_probs = sum(poc_first_probs.values())
    poc_first_probs = {x:p/sum_poc_first_probs for x,p in poc_first_probs.items()}

    #consolidate to only prefixes that are valid based on number of candidates
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in white_first_probs.keys()]):
      consolidated_probs[pref] = sum(
          [white_first_probs[x] for x in white_first_probs if x[:sum(num_candidates)]==pref]
          )
    white_first_probs = consolidated_probs
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in poc_first_probs.keys()]):
      consolidated_probs[pref] = sum(
          [poc_first_probs[x] for x in poc_first_probs if x[:sum(num_candidates)]==pref]
          )
    poc_first_probs = consolidated_probs

    for scenario in scenarios_to_run:
      print("\n", scenario)
      for n in range(num_simulations):
        print('.', end="")
        ballots = []
        ballot_length = len(candidates)

        #white voters white first
        for b in range(int(num_ballots*(1-minority_share)*preference_strengths[1])):
            ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['C', 'D']:
                 candidate_ordering = {
                    'W':list(np.random.permutation(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #white voters poc first
        for b in range(int(num_ballots*(1-minority_share)*(1-preference_strengths[1]))):
            ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['C', 'D']:
                 candidate_ordering = {
                    'W':list(np.random.permutation(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #poc voters poc first
        for b in range(int(num_ballots*(minority_share)*preference_strengths[0])):
            ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['B']:
                 candidate_ordering = {
                    'W':list(reversed(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            elif scenario in ['C']:
                candidate_ordering = {
                   'W':list(np.random.permutation(white_candidates)),
                   'C':list(np.random.permutation(poc_candidates))
                }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #poc voters white first
        for b in range(int(num_ballots*(minority_share)*(1-preference_strengths[0]))):
            ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['B']:
                 candidate_ordering = {
                    'W':list(reversed(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            elif scenario in ['C']:
                candidate_ordering = {
                   'W':list(np.random.permutation(white_candidates)),
                   'C':list(np.random.permutation(poc_candidates))
                }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)
        winners = cw.rcv_run(
            ballots.copy(),
            candidates,
            num_seats,
            cincinnati_transfer,
        )
        poc_elected_Cambridge[scenario].append(len([x for x in winners if x[0] == 'A']))
    return poc_elected_Cambridge


def BABABA(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    scenarios_to_run = ['A', 'B', 'C', 'D']
):
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    poc_candidates = [c for c in candidates if c[0]=='A']
    white_candidates = [c for c in candidates if c[0]=='B']

    def interleave(x,y):
        '''
        Interleaves two lists x and y
        '''
        x = list(x)
        y = list(y)
        minlength = min(len(x), len(y))
        return [z for pair in zip(x[:minlength],y[:minlength]) for z in pair]+x[minlength:]+y[minlength:]

    white_bloc_ballots = {
        'A':[white_candidates+poc_candidates],
        'B':[white_candidates+poc_candidates],
        'C':[list(x)+list(y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[list(x)+list(y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))]
    }
    white_cross_ballots = {
        'A':[interleave(poc_candidates, white_candidates)],
        'B':[interleave(poc_candidates, white_candidates)],
        'C':[interleave(y,x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[interleave(y,x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))]
    }
    poc_bloc_ballots = {
        'A':[poc_candidates+white_candidates],
        'B':[list(x)+white_candidates for x in list(permutations(poc_candidates))],
        'C':[list(y)+list(x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[poc_candidates+white_candidates],
    }
    poc_cross_ballots = {
        'A':[interleave(white_candidates, poc_candidates)],
        'B':[interleave(white_candidates,x) for x in list(permutations(poc_candidates))],
        'C':[interleave(x,y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[interleave(white_candidates, poc_candidates)],
    }

    poc_elected_bababa = {}
    for scenario in scenarios_to_run:
      poc_elected_bababa[scenario] = []
      for n in range(num_simulations):
        babababallots = []
        #poc bloc
        a = int(num_ballots*poc_share*poc_support_for_poc_candidates)
        babababallots.extend(random.choices(poc_bloc_ballots[scenario],k=a))
        #poc cross
        a = int(num_ballots*poc_share*poc_support_for_white_candidates)
        babababallots.extend(random.choices(poc_cross_ballots[scenario],k=a))
        #white bloc
        a = int(num_ballots*(1-poc_share)*white_support_for_white_candidates)
        babababallots.extend(random.choices(white_bloc_ballots[scenario],k=a))
        #white cross
        a = int(num_ballots*(1-poc_share)*white_support_for_poc_candidates)
        babababallots.extend(random.choices(white_cross_ballots[scenario],k=a))
        #winners
        winners = cw.rcv_run(babababallots, candidates, seats_open, cincinnati_transfer)
        poc_elected_bababa[scenario].append(len([w for w in winners if w[0]=='A']))
    return poc_elected_bababa

def luce_gaussian(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    standard_deviation = 0.1
):
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    race_of_candidate = {x:x[0] for x in candidates}
    white_support_vector = [-1 for c in candidates]
    poc_support_vector = [-1 for c in candidates]

    #add noise and reject any support values < 0 or > 1
    while (any([
             (x<0 or x>1) for i in [0,1]
             for x in white_support_vector+poc_support_vector]
           )):
        white_support_vector = []
        poc_support_vector = []
        noise0 = np.random.normal(0,standard_deviation,size=len(candidates))
        noise1 = np.random.normal(0,standard_deviation,size=len(candidates))
        for i, (c, r) in enumerate(race_of_candidate.items()):
            if r == 'A':
                white_support_vector.append((white_support_for_poc_candidates+noise0[i])/num_poc_candidates)
                poc_support_vector.append((poc_support_for_poc_candidates+noise1[i])/num_poc_candidates)
            elif r == 'B':
                white_support_vector.append((white_support_for_white_candidates+noise0[i])/num_white_candidates)
                poc_support_vector.append((poc_support_for_white_candidates+noise1[i])/num_white_candidates)
        #normalize
        norm = sum(white_support_vector)
        white_support_vector = [x/norm for x in white_support_vector]
        norm = sum(poc_support_vector)
        poc_support_vector = [x/norm for x in poc_support_vector]

    #simulate
    poc_elected_luce = []
    for n in range(num_simulations):
        print(".",end="")
        ballots = []
        numballots = num_ballots
        #white
        for i in range(int(numballots*(1-poc_share))):
          ballots.append(
              np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=white_support_vector, replace=False)
          )
        #poc
        for i in range(int(numballots*poc_share)):
          ballots.append(
              np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=poc_support_vector, replace=False)
          )
        #winners
        winners = cw.rcv_run(ballots, candidates, seats_open, cincinnati_transfer)
        poc_elected_luce.append(len([w for w in winners if w[0]=='A']))

    return poc_elected_luce

def luce_dirichlet(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    concentration = 1
):
    alpha = concentration
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    race_of_candidate = {x:x[0] for x in candidates}
    white_support_vector = [-1 for c in candidates]
    poc_support_vector = [-1 for c in candidates]

    noise0 = list(np.random.dirichlet([alpha]*num_candidates[0]))+list(np.random.dirichlet([alpha]*num_candidates[1]))
    noise1 = list(np.random.dirichlet([alpha]*num_candidates[0]))+list(np.random.dirichlet([alpha]*num_candidates[1]))
    support_vec = {
        0:{
            x:(preference_strengths[0]*int(i<num_candidates[0])
            +(1-preference_strengths[0])*int(i>=num_candidates[0]))*noise0[i]
            for i, x in enumerate(candidates)
        },
        1:{
            x:((1-preference_strengths[1])*int(i<num_candidates[0])+
            preference_strengths[1]*int(i>=num_candidates[0]))*noise1[i]
            for i, x in enumerate(candidates)
        },
    }

    #simulate
    poc_elected_luce = []
    for n in range(num_simulations):
        print(".",end="")
        ballots = []
        numballots = num_ballots
        #white
        for i in range(int(numballots*(1-poc_share))):
          ballots.append(
              np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=white_support_vector, replace=False)
          )
        #poc
        for i in range(int(numballots*poc_share)):
          ballots.append(
              np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=poc_support_vector, replace=False)
          )
        #winners
        winners = cw.rcv_run(ballots, candidates, seats_open, cincinnati_transfer)
        poc_elected_luce.append(len([w for w in winners if w[0]=='A']))

    return poc_elected_luce
