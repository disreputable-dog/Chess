import random

class Chess_Piece():
    """Piece Concept"""
    def __init__(self, colour, graphic):
        #checked_path is empty unless a piece can currently 'see' the king. is used for
        #working out checkmates. Possible_moves is where a piece can currently move. Is
        #identical to the return value of available moves (path), apart from path
        #doesn't have pawn forward moves, but unlike possible_moves does have pawn captures
        self.colour = colour
        self.graphic = graphic
        self.possible_moves = []
        self.checked_path = []
        self.move_track = False

    def __repr__(self):
        return self.graphic

    def nesw(self, board, interpreted_coords, turn):
        """Returns cleaned up, right, down, left"""
        x, y = interpreted_coords[0], interpreted_coords[1]
        
        up = [[x, y+i] for i in range(8)]
        right = [[x+i, y] for i in range(8)]
        down = [[x-i, y] for i in range(8)]
        left = [[x, y-i] for i in range(8)]

        #One direction is passed at a time. This is so the game can recognize checkmates
        # - when no check-paths can be blocked
        up_short, up_long = self.conflict_test(up, board, interpreted_coords, turn)
        right_short, right_long = self.conflict_test(right, board, interpreted_coords, turn)
        down_short, down_long = self.conflict_test(down, board, interpreted_coords, turn)
        left_short, left_long = self.conflict_test(left, board, interpreted_coords, turn)


        long_path = up_long + right_long + down_long + left_long
        short_path = up_short + right_short + down_short + left_short

        return short_path, long_path

    def diagonal(self, board, interpreted_coords, turn):
        """Returns cleaned up, right, down, left"""
        x, y = interpreted_coords[0], interpreted_coords[1]
        
        up = [[x+i, y+i] for i in range(8)]
        right = [[x+i, y-i] for i in range(8)]
        down = [[x-i, y-i] for i in range(8)]
        left = [[x-i, y+i] for i in range(8)]

        up_short, up_long = self.conflict_test(up, board, interpreted_coords, turn)
        right_short, right_long = self.conflict_test(right, board, interpreted_coords, turn)
        down_short, down_long = self.conflict_test(down, board, interpreted_coords, turn)
        left_short, left_long = self.conflict_test(left, board, interpreted_coords, turn)

        long_path = up_long + right_long + down_long + left_long
        short_path = up_short + right_short + down_short + left_short

        return short_path, long_path

    def clean(self, clean, own_square):
        """Prevents passing through walls - removes if not between (0,0) - (7,7)"""
        for i in clean:
            if ((i[1]) > 7) or ((i[1]) < 0) or ((i[0]) > 7) or ((i[0]) < 0):
                del (i[:])
                    
        own_square = own_square[0]
                    
        if own_square in clean:
            clean.remove(own_square)
        
        clean = [i for i in clean if i != []]
        
        return clean

    def conflict_test(self, path, board, own_square, turn):
        """Checks if opponent/own piece is in path, from the piece position outwards"""
        long_path = self.clean(path, [own_square])
        short_path = []
        pieces = []
        opposite_colour = next_turn(turn)
        see_king = long_path[:]

        for i in long_path:
            if board[(i[0] + (i[1] * 8))] != "  ":
                if board[(i[0] + (i[1] * 8))].colour == self.colour:
                    pieces.append(long_path.index(i))
                    if pieces:
                        h = pieces[0]
                        for i, val in enumerate(long_path):
                            if i > h:
                                del long_path[i:]

                else:
                    pieces.append(long_path.index(i))
                    if pieces:
                        h = pieces[0]
                        for i, val in enumerate(long_path):
                            if i > h:
                                del long_path[i:]

        long_path_index = [(i[0] + i[1]*8) for i in long_path]

        short_path = long_path[:]

        for i in long_path_index:
            if board[i] != "  ":
                if board[i].colour == turn:
                    short_path = [i for i in long_path[:-1]]

        #if KING_LOCATION[opposite_colour] in long_path:
         #   long_path.append([(long_path[len(long_path)][0] + 1)])

        if KING_LOCATION[opposite_colour] in short_path:
            long_path = see_king

        self.check_path(short_path, turn, own_square)
 
        return short_path, long_path

    def conflict_knight_king(self, board, path, own_square, turn):
        """Compiles move list for knight and kings, which are 'short-ranged' pieces"""
        path = self.clean(path, [own_square])
        new_path = []
        long_path = path[:]

        for i in path:
            if board[(i[0] + (i[1] * 8))] == "  ":
                new_path.append(i)
            elif board[(i[0] + (i[1] * 8))].colour != self.colour:
                new_path.append(i)

        opposite_colour = next_turn(turn)

        if KING_LOCATION[opposite_colour] in new_path:
            self.checked_path.append(own_square)
            #print("checked path is: ",self.checked_path)
        

        return new_path, long_path

    def check_path(self, path, turn, own_square):
        """Compiles a list containing piece paths if those pieces are checking the king"""
        opposite_colour = next_turn(turn)

        if KING_LOCATION[opposite_colour] in path:
            self.checked_path = [own_square] + path
            del self.checked_path[len(self.checked_path) - 1]
            #print("checked path is: ",self.checked_path)

        return None

    def clears_check_path(self, path, turn):
        """Clears the pieces' check path attribute if that piece can't 'see' the king"""
        opposite_colour = next_turn(turn)

        if KING_LOCATION[opposite_colour] not in path:
            self.checked_path.clear()
        else:
            #print("yo.")
            None
            



#---------------------------------------------------------------------------


class Rook(Chess_Piece):
    """Rook Piece"""
    
    def available_moves(self, board, interpreted_coords, turn, location):
        path, long_path = self.nesw(board, interpreted_coords, turn)
        
        self.possible_moves = path
        self.clears_check_path(path, turn)
        self.location = location
        
        return path, self.possible_moves, self.checked_path, long_path

    
class Bishop(Chess_Piece):
    """Bishop Piece"""
     
    def available_moves(self, board, interpreted_coords, turn, location):
        path, long_path = self.diagonal(board, interpreted_coords, turn)
        
        self.possible_moves = path
        self.clears_check_path(path, turn)
        self.location = location
        
        return path, self.possible_moves, self.checked_path, long_path
                  

class Knight(Chess_Piece):
     
    def available_moves(self, board, interpreted_coords, turn, location):
        x = interpreted_coords[0]
        y = interpreted_coords[1]
        path = [[x+1, y+2], [x+2, y+1], [x+2, y-1], [x+1, y-2]
               ,[x-1, y-2], [x-2, y-1], [x-2, y+1], [x-1, y+2]]
                
        path, long_path = self.conflict_knight_king(board, path, interpreted_coords, turn)
        
        self.possible_moves = path
        self.clears_check_path(path, turn)
        self.location = location

        return path, self.possible_moves, self.checked_path, long_path


class Queen(Chess_Piece):
     
    def available_moves(self, board, interpreted_coords, turn, location):
        diag_path, diag_long_path = self.diagonal(board, interpreted_coords, turn)
        card_path, card_long_path = self.nesw(board, interpreted_coords, turn)
        
        self.possible_moves = diag_path + card_path
        long_path = diag_long_path + card_long_path
        
        path = self.possible_moves

        self.clears_check_path(path, turn)
        self.location = location
        
        return path, self.possible_moves, self.checked_path, long_path


class King(Chess_Piece):
     
    def available_moves(self, board, interpreted_coords, turn, location):
        x = interpreted_coords[0]
        y = interpreted_coords[1]
        path = [[x, y+1], [x+1, y+1], [x+1, y], [x+1, y-1]
               ,[x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1]]

        KING_LOCATION[turn] = interpreted_coords

        path, long_path = self.conflict_knight_king(board, path, interpreted_coords, turn)

        self.possible_moves = path
        self.clears_check_path(path, turn)

        poss = []
        
        self.location = location

        return path, poss, self.checked_path, long_path


class Pawn(Chess_Piece):

    def __init__(self, colour, graphic):
        super().__init__(colour, graphic)
        self.diagonals = None
        self.en_passant = False
        
    def available_moves(self, board, interpreted_coords, turn, location):
        x = interpreted_coords[0]
        y = interpreted_coords[1]
        if self.colour == WHITE:
            pawn_move = [[x, y+1], [x, y+2]]
            pawn_capture = [[x+1, y+1], [x-1, y+1]]
        else:
            pawn_move = [[x, y-1], [x, y-2]]
            pawn_capture = [[x-1, y-1], [x+1, y-1]]

        long_path = pawn_capture[:]
        
        pawn_move, pawn_capture = self.pawn_moves(board, interpreted_coords, pawn_move, pawn_capture, turn)

        self.possible_moves = [pawn_move]
        self.possible_moves.append(pawn_capture)
            
        #Need to uncomment this out for it to work
        #if self.en_passant != False:
            #self.possible_moves.append([self.en_passant])
        
        self.possible_moves = [item for sublist in self.possible_moves for item in sublist]
        self.possible_moves = [i for i in self.possible_moves if i != []]

        #print("my possible moves are", self.possible_moves, "and my path is", pawn_capture)

        if self.colour == WHITE:
            diagonals = [[x+1, y+1], [x-1, y+1]]
        else:
            diagonals = [[x-1, y-1], [x+1, y-1]]

        #diagonals = self.clean(diagonals, interpreted_coords)

        #long_path = self.clean(long_path, interpreted_coords)

        self.clears_check_path(diagonals, turn)
        self.location = location
        
        return diagonals, self.possible_moves, self.checked_path, long_path

    def pawn_moves(self, board, own_square, pawn_move, pawn_capture, turn):
        """Contains: moving two squares; capturing and blocking; en pasant; promotion"""
        
        #One square forward  
        if own_square not in PAWN_START_DICT[self.colour]:
            del pawn_move[1]
            if board[(pawn_move[0][0] + (pawn_move[0][1] * 8))] != "  ":
                pawn_move.clear()
                    
        #Two squares forward
        else:
            if board[(pawn_move[0][0] + (pawn_move[0][1] * 8))] != "  ":
                pawn_move.clear()
            if pawn_move:
                if board[(pawn_move[1][0] + (pawn_move[1][1] * 8))] != "  ":
                    del pawn_move[1]
                    
        #Capture
        if str(board[(pawn_capture[1][0] + (pawn_capture[1][1] * 8))]) in PIECEDICT[self.colour].values() or board[(pawn_capture[1][0] + (pawn_capture[1][1] * 8))] == "  ":
            del pawn_capture[1]
            
        #fix problem when white moves to h7
        if pawn_capture[0] == [8, 7]:
            del pawn_capture[0]
        else:    
            if str(board[(pawn_capture[0][0] + (pawn_capture[0][1] * 8))]) in PIECEDICT[self.colour].values() or board[(pawn_capture[0][0] + (pawn_capture[0][1] * 8))] == "  ":
                del pawn_capture[0]
        
        pawn_capture = self.clean(pawn_capture, [own_square])
        pawn_move = self.clean(pawn_move, [own_square])

        opposite_colour = next_turn(turn)

        if KING_LOCATION[opposite_colour] in pawn_capture:
            self.checked_path.append(own_square)
            #print("checked path is: ",self.checked_path)

        return pawn_move, pawn_capture
    
    def promotion_number(self, question, num_input1, num_input2, ai):
        response = None
        num_range = list(range(num_input1, num_input2))
        
        if ai == True:
            response = random.choice(num_range)
            
        while response not in num_range:
            try:
                response = int(input(question))
            except:
                print("You must enter a number")

        return int(response) - 1 
    
    
    def promotion(self, turn, ai):
        #print("PROMOTION. Which piece would you like to promote to?")
        choice = self.promotion_number("Enter '1' for Queen, \n" "Enter '2' for Rook, \n"
                              "Enter '3' for Bishop, \n" "Enter '4 for Knight: ", 1, 5, ai)

        promotion_list = [Queen(turn, PIECEDICT[turn][Queen]), Rook(turn, PIECEDICT[turn][Rook]),
                  Bishop(turn, PIECEDICT[turn][Bishop]), Knight(turn, PIECEDICT[turn][Knight])]

        promoted = promotion_list[choice]
        #print("promoted in piece class is:", promoted)
        
        return promoted
    

def next_turn(turn):
    """Switchs turns."""
    if turn == BLACK:
        return WHITE
    else:
        return BLACK

WHITE = "white"
BLACK = "black"
#PIECEDICT is defined after the classes. It is a dictionary with classes as sub-keys,
#and strings as values

PAWN_START_DICT = {WHITE : [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1]],
                   BLACK : [[0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6]]}

KING_LOCATION = {WHITE : [4, 0], BLACK : [4, 7]}

PIECEDICT = {WHITE : {Rook : "♖", Knight : "♘", Bishop : "♗", Queen : "♕", King : "♔", Pawn : "♙"}, 
             BLACK : {Rook : "♜", Knight : "♞", Bishop : "♝", Queen : "♛", King : "♚", Pawn : "♟"}}


#fsf
