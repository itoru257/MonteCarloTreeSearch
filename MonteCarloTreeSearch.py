"""
Copyright (c) 2018 Toru Ito
Released under the MIT license
http://opensource.org/licenses/mit-license.php
"""

import numpy as np
import math

from Environment import EnvironmentClass

class Node:
    def __init__(self):
        self.action = None
        self.parentNode = None
        self.childNodes = None
        self.values = 0
        self.counts = 0

    def selectChild( self ):

        if self.childNodes is None:

            self.childNodes = []

            for i in range(4):
                child = Node()
                child.action = i
                child.parentNode = self
                
                self.childNodes.append( child )

            return np.random.choice( self.childNodes )

        else:

            for child in self.childNodes:
                if child.counts == 0:
                    return child

            ucb_values = np.zeros( len( self.childNodes ) )

            for i, child in enumerate(self.childNodes):
                ucb_values[i] = child.values / child.counts + math.sqrt( 2.0 * math.log( self.counts ) / child.counts )

            return self.childNodes[ np.argmax( ucb_values ) ]


def updateNode( node, value ):
    while node is not None:
        node.values += value
        node.counts += 1
        node = node.parentNode


"""
Main Program
"""
if __name__ == '__main__':

    env = EnvironmentClass()
    root = Node()

    num_episodes = 50000

    for i in range(num_episodes):

        s = env.reset()
        d = False
        reward = 0
        node = root 

        while d == False:
            node = node.selectChild()
            a = node.action
            s1, reward, d = env.step( a )

        updateNode( node, reward )


    #Print Result
    s = env.reset()
    d = False
    reward = 0
    node = root 

    action_table = np.full( env.observation_space_n, -1 )
    
    while d == False:
        node = node.selectChild()
        a = node.action
        s = env.get_environment_index()
        action_table[s] = a
        s1, reward, d = env.step(a)

    env.print_action( action_table )

    #print( action_table )

    
