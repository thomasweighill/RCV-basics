import pickle
from numpy.random import choice
from collections import defaultdict

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
