# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:06:21 2019

@author: georg
"""

#This asks 'is this the primary file being run, or is it an import? if it is the primary,
#print hello. Useful if a module is used for lots of different things
if __name__ == "__main__":
    print("hello")

import board_class

response = None

while response not in range(1,4):
    response = int(input("Enter 1 for PvP, 2 for PvAI, 3 for AIvAI: "))

#board_obj = board_class.Game(8, response)
#board_obj.main(response)

try:    
    board_obj = board_class.Game(8, response)
    board_obj.main(response)
except:
    print("BROKEN!")
    print(board_obj.board)
    board_obj.display_board(board_obj.board)
    print(board_obj.selected_piece)
    print("Select coords: ", board_obj.selected_piece_coords)
    print("Possible moves: ", board_obj.selected_piece_poss)
    print("move square: ", board_obj.move_square)
    print("move coords: ", board_obj.move_coords)

#The whole game takes place inside the initialiser of Game Board