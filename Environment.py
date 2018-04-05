"""
Copyright (c) 2018 Toru Ito
Released under the MIT license
http://opensource.org/licenses/mit-license.php
"""

"""
Environment
SFFF       (S: starting point, safe)
FHFH       (F: frozen surface, safe)
FFFH       (H: hole, fall to your doom)
HFFG       (G: goal, where the frisbee is located)
"""

"""
Action
0: Left
1: Down
2: Right
3: Up
"""

import numpy as np

class EnvironmentClass:
    def __init__( self ):
        
        self.action_string = ['←', '↓', '→', '↑']

        self.environment = []
        self.environment.extend( [ 'S', 'F', 'F', 'F' ] )         
        self.environment.extend( [ 'F', 'H', 'F', 'H' ] )         
        self.environment.extend( [ 'F', 'F', 'F', 'H' ] )         
        self.environment.extend( [ 'H', 'F', 'F', 'G' ] )         
        
        self.s = [0, 0]
        self.observation_space_n_i = 4
        self.observation_space_n_j = 4
        self.observation_space_n   = 16
        self.action_space_n        = 4

        self.visits = np.zeros( ( self.observation_space_n_i, self.observation_space_n_j ) )

    def get_environment_index( self ):
        return self.s[0] + self.observation_space_n_i * self.s[1]

    def reset( self ):
        self.s = [0, 0]

        self.visits = np.zeros( ( self.observation_space_n_i, self.observation_space_n_j ) )
        self.visits[self.s[0]][self.s[1]] = 1

        return self.get_environment_index()

    def step( self, action ):

        area = False
        
        if action == 0:
            if self.s[0] > 0:
                self.s[0] = self.s[0] - 1 
                area = True

        elif action == 1:
            if self.s[1] < self.observation_space_n_j - 1:
                self.s[1] = self.s[1] + 1 
                area = True
            
        elif action == 2:
            if self.s[0] < self.observation_space_n_i - 1:
                self.s[0] = self.s[0] + 1             
                area = True

        elif action == 3:
            if self.s[1] > 0:
                self.s[1] = self.s[1] - 1 
                area = True
            
        d  = False
        r  = 0.0
        s1 = self.get_environment_index() 
        e = self.environment[s1]

        if area == False:

            d = True
            r = 0.0

        elif e == 'H':

            d = True
            r = 0.0

        elif e == 'G':

            d = True
            r = 1.0

        else:
            
            if self.visits[self.s[0]][self.s[1]] == 1:
                d = True
                r = 0.0
            else:
                self.visits[self.s[0]][self.s[1]] = 1

        return s1, r, d

    def print_action( self, action_table ):
        
        for j in range( self.observation_space_n_j ):
            text = ''

            for i in range( self.observation_space_n_i ):
                s = i + self.observation_space_n_i * j
                e = self.environment[s]

                if e == 'G' or e == 'H': 

                    text += e

                else:
                    
                    a = action_table[s] 

                    if a == -1:
                        text += ' '
                    else:
                        text += self.action_string[a]
    
            print(text)
