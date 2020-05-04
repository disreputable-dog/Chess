# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:53:19 2020

@author: adyeg
"""
import random
import piece_class

#keys are points, values are a 2 item list of index of move, select 
PIECE_MOVE_D = {}


def ai_capture(turn, piece_index, board, coords, passant):
    """The ai will always capture the highest value piece if possible"""

    count = 0
    
    for i in piece_index:
        for y in board[i].possible_moves:
            count += 1
            #For en_passant, which captures without touching the opponent piece
            ai_passant(i, y, turn, passant, board, coords)
            if board[coords.index(y)] != "  ":
                if board[coords.index(y)].colour != turn:
                    PIECE_MOVE_D[board[coords.index(y)].point_value] = [i, coords.index(y)]
                 
    print(count)
    #Toggle this if you want both colours to make capture moves
    if PIECE_MOVE_D != {}:
        select = PIECE_MOVE_D[max(PIECE_MOVE_D.keys())][0]
        move = PIECE_MOVE_D[max(PIECE_MOVE_D.keys())][1]
    else:
        select = random.choice(piece_index)
        move = random.choice(board[select].possible_moves)
        move = (move[0] + (move[1] * 8))
    
    #Toggle this if you want random moves
#    select = random.choice(piece_index)
#    move = random.choice(board[select].possible_moves)
#    move = (move[0] + (move[1] * 8))

    PIECE_MOVE_D.clear()

    return select, move


def ai_passant(i, y, turn, passant, board, coords):
    """Adds the passant move to the PIECE_MOVE_D - as the passant takes without
    touching, this is hard-coded"""
    
    if board[i].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn]:
        if y == passant:
            if turn == "white":
                PIECE_MOVE_D[board[coords.index(y)-8].point_value] = [i, coords.index(y)]
            if turn == "black":
                PIECE_MOVE_D[board[coords.index(y)+8].point_value] = [i, coords.index(y)]
                
    
    



    
    
    


