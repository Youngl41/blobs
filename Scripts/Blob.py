#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 00:52:18 2018

@author: Young
"""



#==============================================================================
# Import Modules
#==============================================================================
import os
import sys
import numpy as np
import pandas as pd
import random as rnd

from copy import deepcopy

main_dir = '/Users/young/Documents/projects/genesis_ai/blobs'
sys.path.append(os.path.join(main_dir, 'scripts/utility'))
from util_simulation import find_possible_actions


#==============================================================================
# Main
#==============================================================================
class Blob:
    def __init__(self, name, time, max_age, coords, value_grid):
        self.name = name
        self.time = time
        self.max_age = max_age
        self.coords = coords
        self.value_grid = value_grid
        self.status = 'Alive'
        
#    def check_status(self):
#        if self.time >= self.max_age:
#            self.status = 'Died of old age'
#            print ('Blob id',str(self.id), 'dead. \t-', self.status)
#            
    def update_and_get_policy(self, grid, beta, alpha=0.2, reroll_chance=0.1):
        possible_action_states = find_possible_actions(grid, self.coords)
        q_values = []
        for action_state in possible_action_states:
            q_value = grid[self.coords] + beta * self.value_grid[action_state]
            q_values.append(q_value)
        q_values = np.array(q_values)
        
        # Take random tie breaking max q values
        max_q_value_idx = np.random.choice(np.flatnonzero(q_values == q_values.max()))
        
        # Best action occurs with x% chance - epsilon greedy algorithm
        reroll_flag = (np.random.uniform() < reroll_chance)
        if reroll_flag:
            random_idx = rnd.sample(range(len(possible_action_states)), 1)[0]
            random_q_value = q_values[random_idx]
            random_action = possible_action_states[random_idx]
            
            # Update value_grid - with temporal difference
            self.value_grid[self.coords] = (1-alpha) * self.value_grid[self.coords] + alpha * random_q_value
            return random_action
        else:
            max_q_value = q_values[max_q_value_idx]
            best_action = possible_action_states[max_q_value_idx]
        
            # Update value_grid - with temporal difference
            self.value_grid[self.coords] = (1-alpha) * self.value_grid[self.coords] + alpha *max_q_value
            return best_action

    def update_and_get_plan(self, grid, beta):
        possible_action_states = find_possible_actions(grid, self.coords)
        q_values = []
        for action_state in possible_action_states:
            q_value = grid[self.coords] + beta * self.value_grid[action_state]
            q_values.append(q_value)
        q_values = np.array(q_values)
        
        # Take random tie breaking max q values
        max_q_value_idx = np.random.choice(np.flatnonzero(q_values == q_values.max()))
        max_q_value = q_values[max_q_value_idx]
        best_action = possible_action_states[max_q_value_idx]
        
        # Update value_grid
        self.value_grid[self.coords] = max_q_value
        return best_action
    
    def update_coords(self, new_coords):
        self.coords = new_coords
        self.time = self.time+1


# =============================================================================
# Unit Test
# =============================================================================
#grid = np.zeros((3,5))
#grid[1][4] = 1
#grid[0] = [-10, -10, -10, -10, -10]
#grid[2] = [-10, -10, -10, -10, -10]
#value_matrix = np.zeros(grid.shape)


#blob = Blob(name = 0, time=0, max_age=30, coords=(1,0), value_grid = np.zeros(g1.grid.shape))
#blob.check_actions_and_update_values(grid=g1.grid, beta=0.5)