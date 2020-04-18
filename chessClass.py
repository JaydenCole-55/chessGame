import math

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
        self.currentMoves  = None
        self.col            = {'a':0, 'b':100, 'c':200, 'd':300, 'e':400, 'f':500, 'g':600, 'h':700}
        self.row            = {'8':0, '7':100, '6':200, '5':300, '4':400, '3':500, '2':600, '1':700}
        self.fn_update_position( position )


    def fn_update_position(self, position):
        # Passed: Some form of position coordinates
        # Returns: None
        # Determines the location of the piece wtihin 1-64 and then calculates the screen position and 
        # chess board location
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
            # ERROR Position passed to update Position was not str or tuple
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
        x = ( ( self.squareNum % 8 ) - 1) * 100
        if x < 0:
            x = 700
        y = ( 8 - math.ceil( self.squareNum / 8 ) ) * 100
        self.screenPosition = (x, y)


    def fn_possible_moves( self ):
        pass


    def fn_update_name( self ):
        pass

class King( Piece ):
    def __init__( self, team, position, image):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "King"
    
    def fn_posible_moves( self ):
        pass

class Queen( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Queen"

    def fn_posible_moves( self ):
        pass

class Rook( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Rook"

    def fn_posible_moves( self ):
        pass

class Knight( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Knight"

    def fn_posible_moves( self ):
        pass

class Bishop( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.name = self.team + "Bishop"

    def fn_posible_moves( self ):
        pass

class Pawn( Piece ):
    def __init__( self, team, position, image ):
        Piece.__init__(self, team, position, image )
        self.fn_update_name()
        if team == 'W':
            self.allMoves = {'U':1, 'U':2, 'UL':1, 'UR':1}
        else:
            self.allMoves = {'D':1, 'D':2, 'DL':1, 'DR':1}

    def fn_posible_moves( self ):
        self.currentMoves = None
        for move in self.allMoves:
            self.currentMoves = self.currentMoves + fn_get_pos_squares( self.allMoves )

    def fn_possible_takes( self ):
        pass

    def fn_update_name( self ):
        self.name = self.team + "Pawn" + self.chessPosition