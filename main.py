# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:06:21 2019

@author: georg
"""

import board_class
import sys
sys.setrecursionlimit(1000)

response = None

while response not in range(1,4):
    response = int(input("Enter 1 for PvP, 2 for PvAI, 3 for AIvAI: "))

count = 0

#for i in range(60):
#    board_obj = board_class.Game(8, response)
#    outcome = board_obj.main(response)
#    print(outcome)
#    count += 1
#    print(count)
    

#for i in range(10000):
try:    
    board_obj = board_class.Game(8, response)
    outcome = board_obj.main(response)
    count += 1
    print(count)
    print(outcome)
except Exception as e:
    print(e)
    print("BROKEN!")
    print(board_obj.board)
    board_obj.display_board(board_obj.board)
    print(board_obj.selected_piece)
    print("Select coords: ", board_obj.selected_piece_coords)
    print("Possible moves: ", board_obj.selected_piece_poss)
    print("move square: ", board_obj.move_square)
    print("move coords: ", board_obj.move_coords)
    input()

#The whole game takes place inside the initialiser of Game Board