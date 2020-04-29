#Loads pathways needs to take turn as an input

#fix being able to promote while in check.Promotion is a fundamental move - can't be commented out
#as it crashes due to piece_class.Pawn indexing

#MAKE THE MOVER MORE MODULAR, THEN UNCOMMENT OUT THE SPECIAL RULES ONE By ONE

#Bug 27th Aug: if move to a square outside of the list, and then selecting the same piece and moving
#somewhere different after it stops you, a bug happens. The mover needs to be more modular

#Do more tests on pins

#When a piece can't move it says 'you can't move there'. For pins, this means
#the piece gets stuck. Should go back to select when this error occurs

#Should be able to change the POSS dict top side. Is ONLY used for intersection
#in checkmates

#Pinning causes the recursion error. 1 solution:. change the path dicts so that they
#contain the square of the pieces. This can then be used if there's an intersection,
#checks if it's still check if the piece which can make the intersection makes it.
#If so, then it is a pinned checkmate

#Currently ai always castles.

#error check the passant. Offers to move to own square move After the passant, then breaks code.
#One improvment to passant would be to add to mover 'if board[move] != to empty'

#En_passant is added to the move list for the next turn. For the current turn, if piece_class.Pawn_move list contains
#an empty square, then that must be the square to passant to. DOESN'T WORK AS PATH CONTAINS MOVES FORWARDS Will still have to add something that
#only accepts it after one turn.

#Can en passant. Now needs something that removes the piece behind, and also removes the
#possibility to passant after one turn has gone.

#31.01.19: fixed the move track by adding 'False' into the check if check

#Promotion has to go after the piece_class.Pawn and the move forward have been done. Then if on backrow, call the
#pieces' promototion method (self.board[move].promotion).

#29.01.19: Finished Castling. Now do Promotion, stalemate, draw by repetition, en passant. 

#27.01.19: issue with move track in mover. Could cause problems - see note

#Should now in the move method: if select piece = King, if castling (either direction) is True,
#if player chooses '1' or '2', call new method which moves the rook and the king

#For the castling_valid method, can pass in negative numbers.

#Castling must be done top-side. Conditions that must be met for castling
#to be added to possible moves:
    #1. Not currently in check
    #2. Not castling through check
    #3. King and rook(s) haven't moved
    #4. Inbetween spaces are empty

#maybe path and poss are the same dictionaty, created bottom-side. Could include long path

#Method for the pieces that removes possible moves if making those moves puts your king in check

#After tnis may need to change the other check code

#path dict may need to have piece_class.Pawn diagonals in it

#path is 'check path', possible moves is what moves a piece can do.
#Different because of piece_class.Pawns

#Flatten list function



import random
import piece_class
import time

class Game_Board():
    """A gameboard of 3x3, 4x4, 5x5, [...]"""

    def __init__(self, num_squares, response):
        self.num_squares = num_squares
        self.board = []
        self.coords = []
        self.chess_coords = []
        self.empty = "  "
        #path dict: possible moves + piece_class.Pawn captures (always left and right capture, regardless of piece being there) + king moves
        #poss dict: possible moves + piece_class.Pawn captures + piece_class.Pawn forwards - king moves
        #check_dict: if a piece is checking the king this is the 'check path' inc. piece own square
        #long_dict includes 'own piece captures' in path
        self.path_dict = None
        self.poss_dict = None
        self.check_dict = None
        self.long_dict = None
        self.rep_counter = 0
        self.cap_counter = 0
        
        self.selected_piece = None
        self.selected_piece_coords = None
        self.selected_piece_poss = None
        self.move_square = None
        self.move_coords = None


    def create_board(self):
        n = (self.num_squares * self.num_squares)
        for i in range(n):
            self.board.append(self.empty)

        for y in range(self.num_squares):
            for x in range(self.num_squares):
                self.coords.append([x, y])

        for i in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            for y in ["a","b","c","d","e","f","g","h"]:
                self.chess_coords.append(y+i)

        #print(self.chess_coords)
    

class Game(Game_Board):
    """Chessboard Class"""

    def main(self, response):

        self.time(START_TIME)
        
        turn = WHITE
        self.create_board()
        self.populate()
        self.loads_pathways(turn)
        
        
#        self.display_board(self.board)
#        print(Game)
        ai = False
        if response == 1:
            self.display_board(self.board)
            while True:
                self.mover(turn, ai)
                self.display_board(self.board)
                #print(turn, " path dict is: ", self.path_dict)
                #print(turn, " poss dict is: ", self.poss_dict[turn])
                #print(turn, " check dict is: ", self.check_dict[turn])
                #print(turn, " long dict is: ", self.long_dict[turn])
                turn = next_turn(turn)
        if response == 2:
            self.display_board(self.board)
            while True:
                self.mover(turn, ai)
                self.display_board(self.board)
                turn = next_turn(turn)
                ai = ai_switch(ai)
        if response == 3:
            ai = True
            self.aivai(ai)
                                
        
    def aivai(self, ai):
        turn = WHITE
        
        while True:
            self.mover(turn, ai)
#            self.display_board(self.board)
            turn = next_turn(turn)
            if sum(COUNT.values()) == 100:
                print("Simulation ended")
                print((COUNT[WHITE] + COUNT[BLACK]), "checkmates, of which white: ",
                      COUNT[WHITE]," and black :", COUNT[BLACK])
                print(COUNT["draw by rep"], "draws by repetition.")
                print(COUNT["draw due to insufficient"], "draw insufficients.")
                print(COUNT["draw due to none in 50"], "draws due to none taken in 50 moves.")
                print(COUNT["draw due to stalemate"], "draws by stalemate")
                print(sum(COUNT.values()), "in total")
                while True:
                    l = ([y - x for x,y in zip(TIME_LIST,TIME_LIST[1:])])
#                    print(l)
                    print(max(l))
                    print(min(l))
                    input()
        
        
    def ask_letter(self, question, ai):
        response = "x"
        letters = ["a","b","c","d","e","f","g","h"]
        
        while response.lower() not in letters:
            response = input(question)
        response = letters.index(response.lower())
        
        return response

    def ask_number(self, question, num_input1, num_input2, ai):
        response = None
        num_range = list(range(num_input1, num_input2))
        
        while response not in num_range:
            try:
                response = int(input(question))
            except:
                self.print_message("You must enter a number")
        
        return int(response) - 1

    def ask_chess_coords(self, question):
        response = input(question).lower()
        while response not in self.chess_coords:
            self.print_message("That's not a valid coordinate")
            response = input(question).lower()
    

        return response[0], response[1]
    
    def chess_coord_moves(self, select):
        """Shows possible moves interpreted as chess coords"""
        hold = []
        
        for i in self.board[select].possible_moves:
            hold.append(self.chess_coords[self.coords.index(i)])
            
        self.print_message(("my possible moves are:",hold))
        
    def print_message(self, message):
        """Prints messages. Makes it easier to turn off when running AI"""
#        print(message)
        pass        

        
    def mover(self, turn, ai):          
        """Moves pieces"""
        
        if ai == False:
            x, y = self.ask_chess_coords("SELECT - Choose chess coord here: ")
            select = self.chess_coords.index(x+str(y))

            
            while (self.board[select] == self.empty or self.board[select].possible_moves == []
              or self.board[select].colour != turn):
                self.print_message("Invalid. Empty square, wrong colour, or the piece cannot move")
                x, y = self.ask_chess_coords("SELECT - Choose chess coord here: ")
                select = self.chess_coords.index(x+str(y))
            selected_piece = self.board[select]
            self.print_message(self.board[select])
            self.chess_coord_moves(select)
        else:
            piece_index = []
            for i in self.board:
                if i != self.empty:
                    if i.colour == turn:
                        if i.possible_moves != []:
                            piece_index.append(self.board.index(i))
            select = random.choice(piece_index)
            selected_piece = self.board[select]
#            print(("The piece you selected is: ",self.board[select], self.coords[select],"the pieces possible moves are: ", self.board[select].possible_moves))
        #updates attributes which can be accessed by the try/except when using AIvAI
        self.selected_piece = self.board[select]
        self.selected_piece_coords = self.coords[select]
        self.selected_piece_poss = self.board[select].possible_moves

        #Offers castling if possible
#        if self.board[select] == self.board[self.coords.index(piece_class.KING_LOCATION[turn])]:
#            if self.board[select].move_track == False:
#                if self.castling(turn, ai):
#                    self.loads_pathways(turn)
#                    self.king_adjust(WHITE)
#                    self.king_adjust(BLACK)
#                    
#                    return None
               
        
        
        if ai == False:
            x, y = self.ask_chess_coords("MOVE - Choose chess coord here: ")
            move = self.chess_coords.index(x+str(y))
            while self.coords[move] not in self.board[select].possible_moves:
                self.print_message("You can't move there")
                self.chess_coord_moves(select)
                x, y = self.ask_chess_coords("MOVE - Choose chess coord here: ")
                move = self.chess_coords.index(x+str(y))
                
            move_square = self.board[move]
        else:
            move = random.choice(self.board[select].possible_moves)
            move = (move[0] + (move[1] * 8))
            move_square = self.board[move]
#            print(("The square you have moved to is: ", move_square, self.coords[move]))
        self.move_square = move_square
        self.move_coords = self.coords[move]
            
            

# =============================================================================
#         if self.board[select].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn]:
#             if move_coords == self.board[select].en_passant:
#                 if turn == WHITE:
#                     self.board[move - 8] = self.empty
#                 else:
#                     self.board[move + 8] = self.empty
# 
# =============================================================================

        #Offers promotion if possible        
        if self.board[select].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn] and self.coords[move] in BACK_ROW_DICT[turn]:
            promotion = self.board[select].promotion(turn, ai)
            self.board[select] = promotion
            #print("promotion in game class is: ", promotion)
            
        #print(self.board[select], self.coords[select], self.coords[move])
        
        #print("self.board[select] = ",self.board[select], "self.board[move] = ",self.board[move])
        
        if self.board[move] != self.empty:
            captured = self.board[move].graphic
        else:
            captured = None
        
        self.board[move] = self.board[select]
        self.board[select] = self.empty
    
        

        #Sets the piece attribute 'en_passant' to true if conditions met Ready for the next turn
        #if board[move] != to empty
         #   if self.board[move].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn]:
          #      if self.coords[move] in EN_PASSANT_DICT[turn]:
           #         if self.board[move].move_track == False:
            #            if self.board[(move + 1)] != self.empty:
             #               if self.board[(move + 1)].graphic == piece_class.PIECEDICT[opposite_turn][piece_class.Pawn] and self.coords[move + 1] in EN_PASSANT_DICT[turn]:
              #                  if turn == BLACK:
               #                     self.board[(move + 1)].en_passant = self.coords[move + 8]
                #                else:
                 #                   self.board[(move + 1)].en_passant = self.coords[move - 8]
#
 #                       if self.board[(move - 1)] != self.empty:
  #                          if self.board[(move - 1)].graphic == piece_class.PIECEDICT[opposite_turn][piece_class.Pawn] and self.coords[move - 1] in EN_PASSANT_DICT[turn]:
   #                             if turn == BLACK:
    #                                self.board[(move - 1)].en_passant = self.coords[move + 8]
     #                           else:
      #                              self.board[(move - 1)].en_passant = self.coords[move - 8]


        if self.coords[select] == piece_class.KING_LOCATION[turn]:
            piece_class.KING_LOCATION[turn] = self.coords[select]
            
        self.loads_pathways(turn)
        #maybe just one with (turn) would work
        self.king_adjust(WHITE)
        self.king_adjust(BLACK)
        
#        if self.board[move] != self.empty:
#            self.board[move].move_track = True
        
        REPETITION_PREV[turn] = [self.coords[select], self.coords[move]]
        
        if self.checks_check(turn):
            self.print_message("Can't move there. That move puts/keeps you in check")
            self.print_message(('move is: ', self.board[move]))
            self.print_message(('select is: ', self.board[select]))
#            self.board[move].move_track = False
            self.board[select] = selected_piece
            self.board[move] = move_square
            
            self.loads_pathways(turn)
            self.king_adjust(WHITE)
            self.king_adjust(BLACK)

            #recursive function
            self.mover(turn, ai)
            
        opposite_turn = next_turn(turn)
        
        if captured == None:
            self.cap_counter += 1
        else:
            CAPTURE_DICT[opposite_turn].append(captured)
            self.cap_counter = 0
            
        self.draw_by_rep(turn, select, move)
        self.draw_by_insufficient()
        self.stalemate(turn)
    
        
        #print("captured dict is: ", CAPTURE_DICT)

        #if self.board[move] != self.empty:
         #   if self.board[move].graphic == piece_class.PIECEDICT[turn][piece_class.Pawn]:
          #      print(turn)
           #     self.display_board(self.board)



      
    def display_board(self, board):
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

    def populate(self):
        """Populates the board with piece objects"""
        counter = 0
        placers = [piece_class.Rook, piece_class.Knight, piece_class.Bishop, 
                   piece_class.Queen, piece_class.King, piece_class.Bishop, 
                   piece_class.Knight, piece_class.Rook, piece_class.Pawn, 
                   piece_class.Pawn, piece_class.Pawn, piece_class.Pawn, 
                   piece_class.Pawn, piece_class.Pawn, piece_class.Pawn, 
                   piece_class.Pawn]
        
        
        #Creates new piece objects
        for i in placers:
            self.board[counter] = (i(WHITE, piece_class.PIECEDICT[WHITE][i]))
            counter += 1
            
        counter = 48
        placers.reverse()
        placers[11], placers[12] = placers[12], placers[11]
        
        for i in placers:
            self.board[counter] = (i(BLACK, piece_class.PIECEDICT[BLACK][i]))
            counter += 1

#        self.board[63] = self.empty
#        self.board[62] = self.empty
#        self.board[61] = self.empty
#        self.board[60] = self.empty
#        self.board[59] = self.empty
#        self.board[58] = self.empty
#        self.board[57] = self.empty
#        self.board[56] = self.empty
#        self.board[55] = self.empty
#        self.board[54] = self.empty
#        self.board[53] = self.empty
#        self.board[52] = self.empty
#        self.board[51] = self.empty
#        self.board[50] = self.empty
#        self.board[49] = self.empty
#        self.board[48] = piece_class.Bishop(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Bishop])
#        self.board[(40-16)] = piece_class.Rook(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Rook])
#        self.board[(41-16)] = piece_class.Rook(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Rook])
##        self.board[(41-7)] = piece_class.Bishop(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Bishop])
#        self.board[56] = piece_class.King(BLACK, piece_class.PIECEDICT[BLACK][piece_class.King])
            
#        self.board[18] = piece_class.Rook(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Rook])
#        self.board[21] = piece_class.Bishop(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Bishop])
#        self.board[27] = piece_class.Bishop(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Bishop])
#        self.board[36] = piece_class.Knight(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Knight])
#        self.board[41] = piece_class.Rook(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Rook])
##        self.board[32] = piece_class.Bishop(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Bishop])
#        self.board[48] = piece_class.King(WHITE, piece_class.PIECEDICT[WHITE][piece_class.King])
##        self.board[59] = piece_class.King(BLACK, piece_class.PIECEDICT[BLACK][piece_class.King])
#        self.board[49] = piece_class.Pawn(WHITE, piece_class.PIECEDICT[WHITE][piece_class.Pawn])
#        self.board[50] = piece_class.Queen(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Queen])
#        self.board[59] = piece_class.Bishop(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Bishop])
#        self.board[52] = piece_class.Pawn(BLACK, piece_class.PIECEDICT[BLACK][piece_class.Pawn])
#    
#        del self.board[64:]

        return self.board

    def loads_pathways(self, turn):
        """Tracks available moves for every piece"""
        black_coords, white_coords = self.parser()
        counter = 0
        path_dict, poss_dict, check_dict, long_dict = {BLACK : [], WHITE : []}, {BLACK : [], WHITE : []}, {BLACK : [], WHITE : []}, {BLACK : [], WHITE : []}
        
        for i in self.board:
            if i != self.empty:
                if i.colour == WHITE:
                    path, poss, checked_path, long_path = i.available_moves(self.board, white_coords[counter], WHITE, self.coords[self.board.index(i)])
                    counter += 1
                    if path != None and path != []:
                        path_dict[WHITE] += path
                    if poss != None and poss != []:
                        poss_dict[WHITE] += poss
                    if checked_path != []:
                        check_dict[WHITE] += (checked_path)
                    if long_path != []:
                        long_dict[WHITE] += long_path

        counter = 0

        for i in self.board:
            if i != self.empty:
                if i.colour == BLACK:
                    path, poss, checked_path, long_path = i.available_moves(self.board, black_coords[counter], BLACK, self.coords[self.board.index(i)])
                    counter += 1
                    if path != None and path != []:
                        path_dict[BLACK] += path
                    if poss != None and poss != []:
                        poss_dict[BLACK] += poss
                    if checked_path != []:
                        check_dict[BLACK] += (checked_path)
                    if long_path != []:
                        long_dict[BLACK] += long_path        
        
        self.path_dict = path_dict
        self.poss_dict = poss_dict
        self.check_dict = check_dict
        self.long_dict = long_dict

    def parser(self):
        """Turns the board index' which hold pieces into coordinates"""
        hold = [i for i, val in enumerate(self.board) if val != self.empty and val.colour == BLACK]
        hold2 = [i for i, val in enumerate(self.board) if val != self.empty and val.colour == WHITE]
        
        #This is why dictionaries are better
        black_coords = []
        white_coords = []
        
        for i in hold:
            black_coords.append(self.coords[i])

        for i in hold2:
            white_coords.append(self.coords[i])
            
        return black_coords, white_coords

    def checks_check(self, turn):
        """Checks to see if a player is in check"""
        opposite_colour = next_turn(turn)

        if piece_class.KING_LOCATION[opposite_colour] in self.path_dict[turn]:
            self.print_message("CHECK!")
#            self.checkmate(turn)
            self.mate_double(turn)
            self.mate_pinned(turn)
            self.mate_normal(turn)

        if piece_class.KING_LOCATION[turn] in self.path_dict[opposite_colour]:
            return True

        else:
            return False
     
    def mate_double(self, turn):
        """Tests if a double check causes a checkmate"""

        opposite_colour = next_turn(turn)
        opp_king_index = (piece_class.KING_LOCATION[opposite_colour][0] + piece_class.KING_LOCATION[opposite_colour][1] * 8)
        opp_poss_moves = {tuple(i) for i in self.poss_dict[opposite_colour]}
        check_path = {tuple(i) for i in self.check_dict[turn]}
        
        if self.board[opp_king_index].possible_moves == []:
            if opp_poss_moves.intersection(check_path) != set():
                double_check = [i for i in self.check_dict[turn] if self.board[self.coords.index(i)] != self.empty]
                if len(double_check) == 2:
                    COUNT[turn] += 1
                    print(sum(COUNT.values()))
                    print("Checkmate.", turn, "wins.")
                    self.display_board(self.board)
                    self.resets_attributes()
                    self.main(3)
#                    Game(8, 3)
                           
    
    def mate_pinned(self, turn):
        """Checks piece(s) are pinned to the king, and can't prevent checkmate"""
        
        pinned_list = []
        opposite_colour = next_turn(turn)
        opp_king_index = (piece_class.KING_LOCATION[opposite_colour][0] + piece_class.KING_LOCATION[opposite_colour][1] * 8)
        opp_poss_moves = {tuple(i) for i in self.poss_dict[opposite_colour]}
        check_path = {tuple(i) for i in self.check_dict[turn]}
        
        if self.board[opp_king_index].possible_moves == []:
            if opp_poss_moves.intersection(check_path) != set():
                for i in self.board:
                    if i != self.empty:
                        if i.colour == opposite_colour:
                            if i.graphic != piece_class.PIECEDICT[opposite_colour][piece_class.King]:
                                if check_path.intersection({tuple(y) for y in i.possible_moves}):
                                    intersec = check_path.intersection({tuple(y) for y in i.possible_moves})
                                    intersec = [list(i) for i in intersec]
                                    for y in intersec:
#                                        self.display_board(self.board)
#                                        
#                                        print(y)
                                        
                                        select = self.coords.index(i.location)
                                        move = self.coords.index(y)
                                        move_square = self.board[move]
                                        selected_piece = self.board[select]
                                        
                                        
                                        if i.graphic == piece_class.PIECEDICT[opposite_colour][piece_class.Pawn] and i.location in piece_class.PAWN_START_DICT[turn]:
                                            self.board[move] = piece_class.Queen(opposite_colour, piece_class.PIECEDICT[opposite_colour][piece_class.Queen])
                                        else:
                                            self.board[move] = self.board[select]
                                            
                                        self.board[select] = self.empty
                                        self.loads_pathways(opposite_colour)
                                        
#                                        self.display_board(self.board)                                        
                                        if piece_class.KING_LOCATION[opposite_colour] in self.path_dict[turn]:
#                                            print("1")
                                            pinned_list.append(1)
                                        else:
#                                            print("0")
                                            pinned_list.append(0)
                                            
                                        self.board[select] = selected_piece
                                        self.board[move] = move_square
                                        
                                        self.loads_pathways(opposite_colour)
                                        
#                                        input()
#                                    intersec = [item for sublist in intersec for item in sublist]
#                print("pinned list is: ", pinned_list)
                
        if pinned_list != [] and 0 not in pinned_list:
#            input("CHECKMATE")
            COUNT[turn] += 1
            print(sum(COUNT.values()))
            print("Checkmate.", turn, "wins.")
            #input()
            #while True:
             #   self.display_board(self.board)
              #  input("Checkmate.", turn, "wins.")
            self.display_board(self.board)
#            Game(8, 3)
            self.resets_attributes()
            self.main(3)
            
    def mate_normal(self, turn):
        """Tests for the most usual checkmate"""
        
        opposite_colour = next_turn(turn)
        opp_king_index = (piece_class.KING_LOCATION[opposite_colour][0] + piece_class.KING_LOCATION[opposite_colour][1] * 8)
        opp_poss_moves = {tuple(i) for i in self.poss_dict[opposite_colour]}
        check_path = {tuple(i) for i in self.check_dict[turn]}
        
        if self.board[opp_king_index].possible_moves == []:
            if opp_poss_moves.intersection(check_path) == set():
                COUNT[turn] += 1
                print(sum(COUNT.values()))
                print("Checkmate.", turn, "wins.")
                #input()
                #while True:
                 #   self.display_board(self.board)
                  #  input("Checkmate.", turn, "wins.")
                self.display_board(self.board)
#                Game(8, 3)
                self.resets_attributes()
                self.main(3)
                    
    def draw_by_rep(self, turn, select, move):
        """Checks if there's a draw by repitition"""
        REPETITION_CURR[turn] = [self.coords[select], self.coords[move]]

        if REPETITION_PREV[turn] != []:
            if REPETITION_CURR[turn][0] == REPETITION_PREV[turn][1] and REPETITION_CURR[turn][1] == REPETITION_PREV[turn][0]:
                self.rep_counter += 1
            else:
                self.rep_counter = 0

        #print(self.rep_counter)
        if self.rep_counter == 6:
            self.draw_loop("draw by rep")
                
    def draw_by_insufficient(self):
        """Checks if there's a draw due to insufficient material"""
        
        if self.cap_counter > 100:
            self.draw_loop("draw due to none in 50")
        
#        if self.board.COUNT(self.empty) == 62:
#            self.draw_loop("draw due to insufficient")
            
        if self.board.count(self.empty) == 61:
            for i in self.board:
                if i != self.empty:
                    if i.graphic == piece_class.PIECEDICT[WHITE][piece_class.Bishop] or i.graphic == piece_class.PIECEDICT[BLACK][piece_class.Bishop]:
                        self.draw_loop("draw due to insufficient")
                    if i.graphic == piece_class.PIECEDICT[WHITE][piece_class.Knight] or i.graphic == piece_class.PIECEDICT[BLACK][piece_class.Knight]:
                        self.draw_loop("draw due to insufficient")
                                    
    def draw_loop(self, draw_type):
        while True: 
            COUNT[draw_type] += 1
            print(sum(COUNT.values()))
            print(draw_type)
            self.display_board(self.board)
#            Game(8, 3)
            self.resets_attributes()
            self.main(3)
            
    def stalemate(self, turn):
        move_list = []
        pinned_list = []
        
        opposite_colour = next_turn(turn)
        for i in self.board:
            if i != self.empty:
                if i.colour == opposite_colour:
                    if i.possible_moves != []:
                        move_list.append(i.possible_moves)
                        
        if move_list == []:
            self.draw_loop("draw due to stalemate")
                        
        opp_king_index = (piece_class.KING_LOCATION[opposite_colour][0] + piece_class.KING_LOCATION[opposite_colour][1] * 8)
        
        if self.board[opp_king_index].possible_moves == []:
            for i in self.board:
                if i != self.empty:
                    if i.colour == opposite_colour:
                        if i.graphic != piece_class.PIECEDICT[opposite_colour][piece_class.King]:
                            for y in i.possible_moves:
#                                self.display_board(self.board)
#                                print("staled pin: ")
#                                print("Location: ", i.location)
#                                print("Graphic: ", i.graphic)
                                select = self.coords.index(i.location)
                                move = self.coords.index(y)
                                move_square = self.board[move]
                                selected_piece = self.board[select]
                                
                                if i.graphic == piece_class.PIECEDICT[opposite_colour][piece_class.Pawn] and i.location in piece_class.PAWN_START_DICT[turn]:
                                    self.board[move] = piece_class.Queen(opposite_colour, piece_class.PIECEDICT[opposite_colour][piece_class.Queen])
#                                    print("yo")
                                else:
                                    self.board[move] = self.board[select]
                                    
                                self.board[select] = self.empty
                                
                                self.loads_pathways(opposite_colour)
                                
#                                        self.display_board(self.board)                                        
                                if piece_class.KING_LOCATION[opposite_colour] in self.path_dict[turn]:
#                                            print("1")
                                    pinned_list.append(1)
                                else:
#                                            print("0")
                                    pinned_list.append(0)
                                
#                                print("Moves to: ", y)
#                                self.display_board(self.board)
                                    
                                self.board[select] = selected_piece
                                self.board[move] = move_square
                                
                                self.loads_pathways(opposite_colour)
                                
#        print("pinned list is: ", pinned_list)
        
        if pinned_list != [] and 0 not in pinned_list:
            self.draw_loop("draw due to stalemate")
                            
        
    def attribute_test(self):
        #print("self.path_dict: ", self.path_dict)
        for i in self.board:
            if i != self.empty:
                if i.graphic == piece_class.PIECEDICT[WHITE][piece_class.Pawn]:
                    print(i.en_passant)
                #print("self.possible_moves: ", i.possible_moves)
                #print("self.checked_path: ", i.checked_path)
                #print("self.colour: ", i.colour)
                
                pass

    def king_adjust(self, turn):
        """Adjusts the king moves to take into account opponent paths"""

        opposite_turn = next_turn(turn)

        original_location_index = (piece_class.KING_LOCATION[turn][0] + piece_class.KING_LOCATION[turn][1] * 8)
        
#        if self.board[original_location_index] == self.empty:
#            print("yo")
        
        self.board[original_location_index].possible_moves = [i for i in self.board[original_location_index].possible_moves if i not in self.long_dict[opposite_turn]]
        


        #king_path = [i for i in self.board[original_location_index].possible_moves if i not in self.path_dict[opposite_turn]]

        #removes moving into check from king path. Can remove this functionality from the move method now.
        #self.board[original_location_index].possible_moves = king_path
        #king_path_index = [(i[0] + i[1]*8) for i in self.board[original_location_index].possible_moves]

        
        #for i in king_path:
         #   if i in self.long_dict[opposite_turn] or self.check_dict[opposite_turn]:
          #      print("king path is: ", king_path)
           #     king_path.remove(i)
            #    print("king path is now: ", king_path)
        




        #for i in king_path_index:
         #   enemy_piece = self.board[i]
          #  self.board[i] = self.board[original_location_index]
           # self.board[original_location_index] = self.empty
           # self.loads_pathways(turn)
           # if self.coords[i] in self.path_dict[opposite_turn]:
            #    print("yo")
                
            #self.board[original_location_index] = self.board[i]
            #self.board[i] = enemy_piece


    def move_track(self):
        for i in self.board:
            if i != self.empty:
                print(i.move_track)

    def castling_valid(self, turn, direction):
        opposite_colour = next_turn(turn)

        if self.board[direction[0]] and self.board[direction[-1]] != self.empty:
            if (self.board[direction[0]].graphic) == piece_class.PIECEDICT[turn][piece_class.King] and (self.board[direction[-1]].graphic) == piece_class.PIECEDICT[turn][piece_class.Rook]:
                if self.board[direction[0]].move_track == False and self.board[direction[-1]].move_track == False:
                    for i in self.path_dict[opposite_colour]:
                        if i in self.coords:
                            if self.coords.index(i) in direction[0:3]:
                                
                                return False
                            
                    if len(direction) == 4:
                        if self.board[direction[1]] and self.board[direction[2]] == self.empty:
                            
                            return True
                        
                    elif len(direction) == 5:
                        if self.board[direction[1]] and self.board[direction[2]] and self.board[direction[3]] == self.empty:
                            
                            return True

        return False

        

    def castling(self, turn, ai):
        castling_left = [self.coords.index(piece_class.KING_LOCATION[turn]), self.coords.index(piece_class.KING_LOCATION[turn]) - 1,
                         self.coords.index(piece_class.KING_LOCATION[turn]) - 2, self.coords.index(piece_class.KING_LOCATION[turn]) - 3,
                         self.coords.index(piece_class.KING_LOCATION[turn]) - 4]
        castling_right = [self.coords.index(piece_class.KING_LOCATION[turn]), self.coords.index(piece_class.KING_LOCATION[turn]) + 1,
                         self.coords.index(piece_class.KING_LOCATION[turn]) + 2, self.coords.index(piece_class.KING_LOCATION[turn]) + 3]
        #print("castling left: ",castling_left)
        #print("castling right: ",castling_right)
        
        if self.castling_valid(turn, castling_right):
            if ai == True:
                choice = "y"
            else:
                choice = input("Can castle kingside. Enter ""y"" to castle Kingside.")
            if choice == "y":
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) + 2] = King(turn, piece_class.PIECEDICT[turn][piece_class.King])
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) + 1] = Rook(turn, piece_class.PIECEDICT[turn][piece_class.Rook])
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn])] = self.empty
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) + 3] = self.empty

                 #Could remove these. Move track is only used for castling
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) + 1].move_track = True
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) + 2].move_track = True

                 piece_class.KING_LOCATION[turn] = self.coords[self.coords.index(piece_class.KING_LOCATION[turn]) + 2]

                 return True
                
            
        if self.castling_valid(turn, castling_left):
            if ai == True:
                choice = "y"
            else:
                choice = input("Can castle queenside. Enter ""y"" to castle Queenside.")
            if choice == "y":
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) - 2] = King(turn, piece_class.PIECEDICT[turn][piece_class.King])
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) - 1] = Rook(turn, piece_class.PIECEDICT[turn][piece_class.Rook])
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn])] = self.empty
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) - 4] = self.empty

                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) - 1].move_track = True
                 self.board[self.coords.index(piece_class.KING_LOCATION[turn]) - 2].move_track = True

                 piece_class.KING_LOCATION[turn] = self.coords[self.coords.index(piece_class.KING_LOCATION[turn]) - 2]

                 return True
             
    def resets_attributes(self):
        """Resets all attributes after a game has been played by AIvAI"""
        
        self.path_dict = None
        self.poss_dict = None
        self.check_dict = None
        self.long_dict = None
        self.rep_counter = 0
        self.cap_counter = 0
        
        self.board = []
        self.coords = []
        self.chess_coords = []
        self.empty = "  "
        
        
    def time(self, start_time):
        """Calculates how long a game takes"""
    
        TIME_LIST.append((time.time() - start_time))
        print("--- %s seconds ---" % (time.time() - start_time))
        
        
        

#------------------------------------------------------------------------------------
def next_turn(turn):
    """Switchs turns."""
    if turn == BLACK:
        return WHITE
    else:
        return BLACK

def ai_switch(ai):
    if ai == True:
        ai = False
    else:
        ai = True

    return ai  


START_TIME = time.time()
TIME_LIST = []
             
WHITE = "white"
BLACK = "black"
turn = WHITE

REPETITION_PREV = {WHITE : [], BLACK : []}
REPETITION_CURR = {WHITE : [], BLACK : []}


BACK_ROW_DICT = {BLACK : [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                 WHITE : [[0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7]]}

EN_PASSANT_DICT = {WHITE : [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3]],
                   BLACK : [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4]]}

CAPTURE_DICT = {WHITE : [], BLACK : []}

COUNT = {"checkmate" : 0, "draw by rep" : 0, "draw due to insufficient" : 0,
         "draw due to none in 50" : 0, "draw due to stalemate" : 0, WHITE : 0, BLACK : 0}
