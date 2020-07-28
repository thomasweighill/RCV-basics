# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:28:28 2020

@author: darac
"""
import pandas as pd
import numpy as np
from numpy.random import choice
import random
from additional_funcs import remove_cand

def cincinnati_transfer(cand, ballot_list, win_lose, cutoff):
    if win_lose == 'lose':
        remove_cand(cand, ballot_list)
    else:           
        cand_ballots_index = []
        for n, ballot in enumerate(ballot_list):
            if ballot[0] == cand:
                cand_ballots_index.append(n)
        rand_winners = random.sample(cand_ballots_index, int(cutoff))
        #remove winning ballots from simulation
        for index in sorted(rand_winners, reverse = True):
            del ballot_list[index]  
        #remove candidate from rest of ballots
        remove_cand(cand, ballot_list)