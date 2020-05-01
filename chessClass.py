import math

def fn_check_empty( squareNums, pieces ):
    # Passed: list of squareNums, the pieces
    # Returns: bool
    # Checks if a list of squares is empty
    empty = True
    for square in squareNums:
        for piece in pieces:
            if piece.squareNum == square:
                empty = False
                break
        if not empty:
            break
    
    return empty

def fn_check_piece_is_there( name, squareNum, pieces ):
    # Passed: name of a piece, a position, the pieces
    # Returns: bool
    # Checks if the piece is at the squareNum requested
    for piece in pieces:
        if piece.squareNum == squareNum:
            return name in piece.name
    
    return False

def fn_check_moved( squareNum, pieces ):
    # Passed: squareNum
    # Returns: bool
    # Returns if the piece in the square has moved
    for piece in pieces:
        if piece.squareNum == squareNum:
            return piece.hasMoved


def fn_pawn_can_take( pawnPiece, pieces, square ):
    # Passed: A pawn, the pieces, int
    # Returns: if the pawn has a piece it can take on that square
    pieceThere = False
    for piece in pieces:
        if piece.squareNum == square and pawnPiece.team != piece.team:
            return True

    return False


def fn_last_moved( squareNum, pieces ):
    # Passed: SquareNum, pieces
    # Returns: bool
    # Tells if the piece at that sqaure num was the last move
    for piece in pieces:
        if piece.squareNum == squareNum:
            return piece.lastMoved
    
    return None


def fn_last_chess_position( squareNum, pieces ):
    # Passed: int, pieces, int
    # Returns: int
    # Returns the last position where a piece was
    for piece in pieces:
        if piece.squareNum == squareNum:
            return piece.lastChessPos
    
    return None


def fn_check_en_passent( squareNum, team, pieces ):
    # Passed: square number, a team, the pieces
    # Returns: bool
    # Checks if the piece at that sqaure number can be en passented

    for piece in pieces:
        if piece.squareNum == squareNum:
            if team == "W":
                if fn_check_piece_is_there( "BPawn", squareNum, pieces ):
                    return fn_last_moved( squareNum, pieces ) and "7" in fn_last_chess_position( squareNum, pieces )
            elif team == "B":
                if fn_check_piece_is_there( "WPawn", squareNum, pieces ):
                    return fn_last_moved( squareNum, pieces ) and "2" in fn_last_chess_position( squareNum, pieces )
    
    # No pieces at that square number
    return False


class Piece():
    def __init__ (self, team, position, image):
        self.team           = team
        self.image          = image
        self.rect           = None
        self.name           = None
        self.squareNum      = None
        self.chessPosition  = None
        self.screenPosition = None
        self.allMoves       = None
        self.currentMoves   = None
        self.abbrv          = None
        self.lastMoved      = False
        self.lastSquareNum  = None
        self.lastChessPos   = None
        self.col            = {'a':0, 'b':100, 'c':200, 'd':300, 'e':400, 'f':500, 'g':600, 'h':700}
        self.row            = {'8':0, '7':100, '6':200, '5':300, '4':400, '3':500, '2':600, '1':700}
        self.fn_update_position( position )

    def fn_update_position(self, position):
        # Passed: Some form of position coordinates
        # Returns: None
        # Determines the location of the piece wtihin 1-64 and then calculates the screen position and 
        # chess board location

        # Keep track of where the piece has been
        self.lastChessPos  = self.chessPosition
        self.lastSquareNum = self.squareNum

        if isinstance(position, str):
            # Turns chess string into screen coord tuple, then call itself using the tuple
            x = self.col[position[0]]
            y = self.row[position[1]]
            self.fn_update_position( (x,y) )
        elif isinstance(position, tuple):
            # Update what square number its on
            x = position[0]
            y = position[1]
            self.squareNum = 64 - 8 * (math.floor( y/100 )+1) + math.floor( x/100 ) + 1
        elif isinstance( position, int ):
            self.squareNum = position
        else:
            # ERROR Position passed to update Position was not str, tuple, or int
            print("ERROR: " + piece.name + " did not update it's position porperly.")

        # Update the other methods of displaying position - based on the square number
        self.fn_chessboard_location()
        self.fn_screen_position()


    def fn_chessboard_location( self ):
        # Passed: None
        # Returns: None
        # Updates piece's chess location based on its square number
        chessColumns = { 1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 0:'h' }
    
        col = chessColumns[ (self.squareNum % 8) ]
        row = math.ceil( self.squareNum / 8 )
        chessLoc = str(col) + str(row)
        self.chessPosition = chessLoc
        self.fn_update_name()


    def fn_screen_position( self ):
        # Passed: None
        # Returns: None
        # Updates piece's screen loacation based on its square number
        x = ( ( self.squareNum % 8 ) - 1) * 100
        if x < 0:
            x = 700
        y = ( 8 - math.ceil( self.squareNum / 8 ) ) * 100
        self.screenPosition = (x, y)


    def fn_possible_moves( self, pieces ):
        # Passed: self, the other pieces
        # Returns: List of squareNums
        # Determines what squareNums this piece can move to
        possibleMoves = []
        jumping = False
        for move in self.allMoves:
            for length in self.allMoves[ move ]:
                if move == 'U':
                    square = self.squareNum + 8 * length
                    if "Pawn" in self.name and "2" not in self.chessPosition and length == 2:
                        # Pawn is not on 2nd rank, cannot move 2 squares
                        continue
                    elif "Pawn" in self.name and not fn_check_empty( [square], pieces):
                        # Square is not empty, pawn cannot move there
                        continue
                    elif "Pawn" in self.name and length == 2 and not fn_check_empty( [square, square-8], pieces ):
                        # Pawn first move is length 2, check if its entire path is empty
                        continue

                elif move == 'UL':
                    square = self.squareNum + 8 * length - length
                    if square % 8 == 0 or ( "Pawn" in self.name and not fn_pawn_can_take( self, pieces, square ) ):
                        # Went around board, or not a valid pawn move, end this move direction
                        break

                elif move == 'L':
                    square = self.squareNum - length
                    if square % 8 == 0:
                        # Went around board, end this move direction
                        break

                elif move == 'DL':
                    square = self.squareNum - 8 * length - length
                    if square % 8 == 0 or ( "Pawn" in self.name and not fn_pawn_can_take( self, pieces, square ) ):
                        # Went around board, or not a valid pawn move, end this move direction
                        break

                elif move == 'D':
                    square = self.squareNum - 8 * length
                    if "Pawn" in self.name and "7" not in self.chessPosition and length == 2:
                        # Pawn not on 7th rank, cannot move 2 squares
                        continue
                    elif "Pawn" in self.name and not fn_check_empty( [square], pieces):
                        # Square is not empty, pawn cannot move there
                        continue
                    elif "Pawn" in self.name and length == 2 and not fn_check_empty( [square, square+8], pieces ):
                        # Pawn first move is length 2, check if its entire path is empty
                        continue

                elif move == 'DR':
                    square = self.squareNum - 8 * length + length
                    if square % 8 == 1 or ( "Pawn" in self.name and not fn_pawn_can_take( self, pieces, square ) ):
                        # Went around board, or not a valid pawn move, end this move direction
                        break
                
                elif move == 'R':
                    square = self.squareNum + length
                    if square % 8 == 1:
                        # Went around board, end this move direction
                        break

                elif move == 'UR':
                    square = self.squareNum + 8 * length + length
                    if square % 8 == 1 or ( "Pawn" in self.name and not fn_pawn_can_take( self, pieces, square ) ):
                        # Went around board, or not a valid pawn move, end this move direction
                        break

                elif move == 'K':
                    jumping = True
                    # Skip specific moves if the piece will move around the side of the board
                    if length == -10 or length == 6:
                        if self.squareNum % 8 == 1 or self.squareNum % 8 == 2:
                            continue
                    elif length == -17 or length == 15:
                        if self.squareNum % 8 == 1:
                            continue
                    elif length == 17 or length == -15:
                        if self.squareNum % 8 == 0:
                            continue
                    elif length == 10 or length == -6:
                        if self.squareNum % 8 == 7 or self.squareNum % 8 == 0:
                            continue
                    # Piece won't wrap around left or right
                    square = self.squareNum + length

                elif move == 'KC': # King side castle
                    if self.hasMoved == False:
                        if self.team == 'W':
                            if fn_check_empty( [6,7], pieces ) and fn_check_piece_is_there( 'WRook', 8, pieces ) and not fn_check_moved( 8, pieces ):
                                square = 7
                        else:
                            if fn_check_empty( [62,63], pieces ) and fn_check_piece_is_there( 'BRook', 64, pieces ) and not fn_check_moved( 64, pieces ):
                                square = 63
                
                elif move == 'QC': # Queen side castle
                    if self.hasMoved == False:
                        if self.team == 'W':
                            if fn_check_empty( [2,3,4], pieces ) and fn_check_piece_is_there( 'WRook', 1, pieces ) and not fn_check_moved ( 1, pieces ):
                                square = 3
                        else:
                            if fn_check_empty( [58,59,60], pieces ) and fn_check_piece_is_there( 'BRook', 57, pieces ) and not fn_check_moved ( 57, pieces ):
                                square = 59
                
                elif move == 'EN': # En passant
                    goodMove = False
                    if self.team == "W" and "5" in self.chessPosition:
                        # Check if there are pawns next to it and if they last moved
                        if length == 1 and ( self.squareNum + 1) % 8 != 1:
                            goodMove = fn_check_en_passent( self.squareNum + 1, self.team, pieces )
                            square = self.squareNum + 9
                        elif length == 2 and ( self.squareNum - 1) % 8 != 0:
                            goodMove = fn_check_en_passent( self.squareNum - 1, self.team, pieces )
                            square = self.squareNum + 7
                    
                    elif self.team == "B" and "4" in self.chessPosition:
                        if length == 1 and ( self.squareNum + 1) % 8 != 1:
                            goodMove = fn_check_en_passent( self.squareNum + 1, self.team, pieces )
                            square   = self.squareNum - 7
                        elif length == 2 and ( self.squareNum - 1) % 8 != 0:
                            goodMove = fn_check_en_passent( self.squareNum - 1, self.team, pieces )
                            square   = self.squareNum - 9

                    if not goodMove:
                        continue
                
                # Check if square is on the board (checks U and D directions)
                if square < 0 or square > 64:
                    continue
                
                pieceInWay = False
                for piece in pieces:
                    if piece.squareNum == square:
                        pieceInWay = True
                        if piece.team == self.team:
                            # Same team cannot move there or through them
                            break
                        else:
                            # Other team, can move there, but not through them
                            possibleMoves = possibleMoves + [ square ]
                            break
                
                if move != 'K' and pieceInWay:
                    # Stop checking in this direction, a piece is in this direction
                    break
                elif move == 'K' and pieceInWay:
                    # Knight move, do not break. Need to check rest of knight moves
                    continue

                # No piece is there and it is on the board, possible move
                possibleMoves = possibleMoves + [ square ]
        
        return possibleMoves
    

    def fn_update_name( self ):
        pass


class King( Piece ):
    def __init__( self, team, position, image):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "King"
        self.allMoves = { 'U':[1], 'UL':[1], 'L':[1], 'DL':[1], 'D':[1], 'DR':[1], 'R':[1], 'UR':[1], 'KC':[1], 'QC':[1] }
        self.hasMoved = False
        self.abbrv    = 'K'


class Queen( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Queen"
        self.allMoves = { 'U':[1,2,3,4,5,6,7], 'UL':[1,2,3,4,5,6,7], 'L':[1,2,3,4,5,6,7], 'DL':[1,2,3,4,5,6,7], 'D':[1,2,3,4,5,6,7], 'DR':[1,2,3,4,5,6,7], 'R':[1,2,3,4,5,6,7], 'UR':[1,2,3,4,5,6,7] }
        self.abbrv    = 'Q'


class Rook( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Rook"
        self.allMoves = { 'U':[1,2,3,4,5,6,7], 'L':[1,2,3,4,5,6,7], 'D':[1,2,3,4,5,6,7], 'R':[1,2,3,4,5,6,7] }
        self.hasMoved = False
        self.abbrv    = 'R'


class Knight( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Knight"
        self.allMoves = { 'K':[-17,-15,-10,-6,6,10,15,17] }
        self.abbrv    = 'N'


class Bishop( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Bishop"
        self.allMoves = { 'UL':[1,2,3,4,5,6,7], 'DL':[1,2,3,4,5,6,7], 'DR':[1,2,3,4,5,6,7], 'UR':[1,2,3,4,5,6,7] }
        self.abbrv    = 'B'


class Pawn( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.fn_update_name()
        self.abbrv    = ''
        if team == 'W':
            self.allMoves = {'U':[1,2], 'UL':[1], 'UR':[1], 'EN':[1,2]}
        else:
            self.allMoves = {'D':[1,2], 'DL':[1], 'DR':[1], 'EN':[1,2]}

    def fn_update_name( self ):
        self.name = self.team + "Pawn" + self.chessPosition