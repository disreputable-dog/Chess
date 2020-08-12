# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:53:19 2020

@author: adyeg
"""
import random
import piece_class
import board_class
    
#keys are points, values are a 2 item list of index of move, select 
piece_move_d = {}
points = {"white" : 0, "black" : 0}
minimax = []
count = 0


def ai_main(turn, piece_index, board, coords, passant):
    """Calls the other AI functions"""
    
    start_branch(turn, piece_index, board, coords, passant)
    one_deep(turn, board, coords)
    
    select = random.choice(piece_index)
    move = random.choice(board[select].possible_moves)
    move = (move[0] + (move[1] * 8))
    
    piece_move_d.clear()
    print("minimax is: ", minimax)
    minimax.clear()
    
    print("EXITING MODULE")
    
    return select, move


def start_branch(turn, piece_index, board, coords, passant):
    """Starts 1 MOVE DEEP. Generates a dict of all possible moves, with 
    positions plus points"""

    count = 0
    
    for i in piece_index:
        for y in board[i].possible_moves:
            count += 1
            #For en_passant, which captures without touching the opponent piece
#            passant_f(i, y, turn, passant, board, coords)
            if board[coords.index(y)] != "  ":
                if board[coords.index(y)].colour != turn:
                    piece_move_d[i, coords.index(y)] = board[coords.index(y)].point_value
                 
    print(count)
    #Toggle this if you want both colours to make capture moves
#    if piece_move_d != {}:
#        select = piece_move_d[max(piece_move_d.keys())][0]
#        move = piece_move_d[max(piece_move_d.keys())][1]
#    else:
#        select = random.choice(piece_index)
#        move = random.choice(board[select].possible_moves)
#        move = (move[0] + (move[1] * 8))
    
    #Toggle this if you want random moves
#    select = random.choice(piece_index)
#    move = random.choice(board[select].possible_moves)
#    move = (move[0] + (move[1] * 8))
        

def one_deep(turn, board, coords):
    
    print("start here", turn, piece_move_d)
    
    for i in piece_move_d:
        print(coords[list(i)[0]], coords[list(i)[1]])
        selected_piece = board[list(i)[0]]
        captured_piece = board[list(i)[1]]
#        capture(turn, board, list(i)[1])
        
        board[list(i)[1]] = board[list(i)[0]]
        board[list(i)[0]] = "  "
        
        print(selected_piece, captured_piece)
        minimax.append(piece_move_d[i])
        print(minimax)
        two_deep(turn, board, coords)
        print("minimax after two_deep: ", minimax)
        
        board[list(i)[0]] = selected_piece
        board[list(i)[1]] = captured_piece
    
    print(points)


def two_deep(turn, board, coords):
    """Looks at responses"""
    
    display_board(board)
    input("starting two deep...")
    
    opposite_turn = board_class.next_turn(turn)
    for i in board:
        if i != "  ":
            if i.colour == opposite_turn:
                for y in i.possible_moves:
                    if board[coords.index(y)] != "  ":
                        if board[coords.index(y)].colour == turn:
                            minimax.append(board[coords.index(y)].point_value)
                            display_board(board)
                            input()
    print("ending two deep")
    
    
def capture(turn, board, move):
    
    if board[move] != "  ":
        points[turn] += board[move].point_value
        

def passant_f(i, y, turn, passant, board, coords):
    """Adds the passant move to the piece_move_d - as the passant takes without
    touching, this is hard-coded"""
    
    if board[i].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn]:
        if y == passant:
            if turn == "white":
                piece_move_d[i, coords.index(y)] = board[coords.index(y)-8].point_value
            if turn == "black":
                piece_move_d[i, coords.index(y)] = board[coords.index(y)+8].point_value
                
            print("passant piece move d: ", piece_move_d)
                
    
def display_board(board):
    """Display game board on screen"""
    
    print("\n\t   - A - B -  C - D -  E -  F -  G -  H - \n")
    print("\t8  ", board[56], "|", board[57], "|", board[58], "|", board[59], "|", board[60], "|", board[61], "|", board[62], "|", board[63])
    print("\t  ", "---------------------------------------")
    print("\t7  ", board[48], "|", board[49], "|", board[50], "|", board[51], "|", board[52], "|", board[53], "|", board[54], "|", board[55])
    print("\t  ", "---------------------------------------")
    print("\t6  ", board[40], "|", board[41], "|", board[42], "|", board[43], "|", board[44], "|", board[45], "|", board[46], "|", board[47])
    print("\t  ", "---------------------------------------")
    print("\t5  ", board[32], "|", board[33], "|", board[34], "|", board[35], "|", board[36], "|", board[37], "|", board[38], "|", board[39])
    print("\t  ", "---------------------------------------")
    print("\t4  ", board[24], "|", board[25], "|", board[26], "|", board[27], "|", board[28], "|", board[29], "|", board[30], "|", board[31])
    print("\t  ", "---------------------------------------")
    print("\t3  ", board[16], "|", board[17], "|", board[18], "|", board[19], "|", board[20], "|", board[21], "|", board[22], "|", board[23])
    print("\t  ", "---------------------------------------")
    print("\t2  ", board[8], "|", board[9], "|", board[10], "|", board[11], "|", board[12], "|", board[13], "|", board[14], "|", board[15])
    print("\t  ", "---------------------------------------")
    print("\t1  ", board[0], "|", board[1], "|", board[2], "|", board[3], "|", board[4], "|", board[5], "|", board[6], "|", board[7])
    print("\n\t   - A - B -  C - D -  E -  F -  G -  H - \n")
    
    
    
        
        
        
    
    
