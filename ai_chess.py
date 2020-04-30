# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:53:19 2020

@author: adyeg
"""
import random
import piece_class


def ai_capture(turn, piece_index, board, coords):
    """The ai will always capture the highest value piece if possible"""

    piece_move_d = {}
    
    for i in piece_index:
        for y in board[i].possible_moves:
            if board[coords.index(y)] != "  ":
                if board[coords.index(y)].colour != turn:
                    piece_move_d[board[coords.index(y)].point_value] = [i, coords.index(y)]
                 

    #Toggle this if you want both colours to make capture moves
    if piece_move_d != {}:
        select = piece_move_d[max(piece_move_d.keys())][0]
        move = piece_move_d[max(piece_move_d.keys())][1]
    else:
        select = random.choice(piece_index)
        move = random.choice(board[select].possible_moves)
        move = (move[0] + (move[1] * 8))
    
    #Toggle this if you want random moves
#    select = random.choice(piece_index)
#    move = random.choice(board[select].possible_moves)
#    move = (move[0] + (move[1] * 8))
    
    return select, move