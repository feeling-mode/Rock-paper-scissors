# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:54:10 2020

@author: Franka
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 00:05:15 2020

@author: Franka
"""

# =============================================================================
# Legend:
#     x - scissors
#     o - rock
#     c - paper
# 
# LET'S PLAY A GAME!
# =============================================================================

import numpy as np
import random

# _____________________________________________________________________________

class Player:
    
    def __init__(self, name):
        self.name = name
        self.__count_table = np.ones((3,3)) #state table
        self.__emit_table = np.zeros((3,3))+1/3 #emition table
        self.__prev_fig = ''
        self.__figures = "" # set if Player plays figures chosen by user
        self.__random_mode = False


    def set_figures(self, figures):
        self.__figures = figures
        
    def turn_on_random_mode(self):
        self.__random_mode=True

    def play_figure(self, index):
        if self.__figures != "":
            return self.__play_given_figure(index)
        elif self.__random_mode == True:
            return self.__play_random_figure()
        elif index<1 :
            return self.__play_random_figure()
        else:
            return self.__play_predicted_figure()
        
    def learn(self, figure, index):
        # update the choice based on oponent's currently played figure and previously played figure      
        if index>0: 
            self.__update_tables(figure)
        self.__memorize(figure) # set just played fig as prev fig
        # print(self.__x_count, self.__o_count, self.__c_count)
        
    def __play_predicted_figure(self): 
        # from learned states
        prev_fig_num = self.__get_num_from_fig(self.__prev_fig)
        next_fig_prob_array = self.__emit_table[prev_fig_num,:] 
        pred_fig=np.random.choice(['x','o','c'], 1, p=next_fig_prob_array)
        fig_to_play = self.__get_win(pred_fig[0]) #gotta play win-over-predicted figure        
        return fig_to_play    
    
    def __get_fig_from_num(self, num):
        switcher = {
            0:'x',
            1:'o',
            2:'c' }
        return switcher.get(num, "Invalid number")
    
    def __get_num_from_fig(self, fig):
        switcher = {
            'x': 0,
            'o': 1,
            'c': 2 }
        return switcher.get(fig, "Invalid figure")
    
    def __check_validity_of_fig(self, fig):
        if fig != 'x' and fig != 'o' and fig != 'c':
            raise ValueError("Figure unknown")
        
    def __play_given_figure(self, index): 
        fig = self.__figures[index]
        self.__check_validity_of_fig(fig)
        return fig
    
    def __play_random_figure(self):
        figures = ["c", "o", "x"]
        return random.choice(figures)
        
    def __get_win(self, fig1):
        switcher = {
        'x': 'o',
        'o': 'c', 
        'c': 'x'    
        }
        return switcher.get(fig1, "Invalid figure")
    
    def __memorize(self, figure):
        self.__prev_fig = figure
        
    
    def __update_tables(self, fig):
        row_num = self.__get_num_from_fig(self.__prev_fig)
        col_num = self.__get_num_from_fig(fig)
        self.__count_table[row_num, col_num] += 1
        self.__emit_table[row_num, :] = self.__count_table[row_num, :]/np.sum(self.__count_table[row_num, :])
        
        
    def get_count_table(self) :
        # return print(self.__count_table)
        return print('\n\tx\t o\t c\t \nx ',self.__count_table[0,:],'\no',self.__count_table[1,:],'\nc',self.__count_table[2,:])

    def get_emit_table(self) :
        # return print(self.__count_table)
        return print('\n\tx\t o\t c\t \nx ',self.__emit_table[0,:],'\no',self.__emit_table[1,:],'\nc',self.__emit_table[2,:])

# _____________________________________________________________________________


class Game:         
        
    def play(self, rounds, pl1, pl2):
        pl1_score=0
        pl2_score=0

        for round in range( rounds ):
            fig1 = pl1.play_figure(round)
            fig2 = pl2.play_figure(round)
            
            pl1_score+=self.__get_points(fig1, fig2)
            pl2_score+=(-1)*self.__get_points(fig1, fig2)
            
            print("Round "+str(round))
            print(pl1.name, ' plays: ', fig1)
            print(pl2.name, ' plays: ', fig2)
            print('')
            
            pl1.learn(fig2, round) 
            pl2.learn(fig1, round)
            
            print(pl1.name) #thoughts for next round?
            pl1.get_emit_table()
            print('\n')
            print(pl2.name) 
            pl2.get_emit_table()
            print('===================================\n')
            
            # if round%5==0 or round==rounds-1:            
            print("Round "+str(round)+" ---> "+pl1.name+": "+str(pl1_score)+", "+pl2.name+": "+str(pl2_score) )
            print('===================================\n')
                
        winner = np.where(pl1_score > pl2_score, pl1.name, np.where(pl1_score==pl2_score, "remis", pl2.name))
        print("THE WINNER IS: " + str(winner))
         
    def __get_points(self, fig1, fig2):
        switcher = {
        'xx': 0,
        'xo': -1, 
        'xc': 1,
        'ox': 1, 
        'oo': 0, 
        'oc': -1, 
        'cx': -1, 
        'co': 1, 
        'cc': 0       
        }
        return switcher.get(str(fig1)+str(fig2), "Invalid figure")
# _____________________________________________________________________________


def main():
    pl1= Player("Player 1")
    pl2= Player("Player 2")
    figures='xxxxxxxxxxxxxxxxxxxxxx'
    # pl1.set_figures(figures)
    rounds=len(figures)
    # pl1.turn_on_random_mode()
    rounds=1000
    
    game = Game()
    game.play(rounds, pl1, pl2)
# _____________________________________________________________________________
    
    
if __name__ == '__main__':
    main()
    