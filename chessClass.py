import math

class Piece():
    def __init__ (self, team, position, image):
        self.team      = team
        self.image     = image
        self.col       = {'a':0, 'b':100, 'c':200, 'd':300, 'e':400, 'f':500, 'g':600, 'h':700}
        self.row       = {'8':0, '7':100, '6':200, '5':300, '4':400, '3':500, '2':600, '1':700}
        self.position  = position
        self.fn_update_position( position )
        self.rect      = None
        self.name      = None

    def fn_update_position(self, position):
        if isinstance(position, str):
            self.fn_screenPosition( position )
            self.position = position
        elif isinstance(position, tuple):
            self.screenPos = self.fn_allign_position( position )
            self.fn_update_chessboard_location( position )
        else:
            # ERROR Position passed to update Position was not str or tuple
            print("ERROR: " + piece.name + " did not update it's position porperly.")

    def fn_screenPosition( self, chessPosition ):
        x = self.col[chessPosition[0]]
        y = self.row[chessPosition[1]]
        self.screenPos = (x,y)

    def fn_update_chessboard_location(self, xypos):
        chess_columns = { 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h' }
    
        col = chess_columns[ math.floor( xypos[0] / 100 ) ]
        row = 7 - math.floor( xypos[1] / 100 ) + 1
        chessLoc = str(col) + str(row)
        self.position = chessLoc
        self.fn_update_name()

    def fn_possible_moves( self ):
        pass

    def fn_update_name( self ):
        pass

    def fn_allign_position(self, xypos):
        # Passed:  tuple of screen coords
        # Returns: coords of the top left pixel of that chess square

        col = math.floor( xypos[0] / 100 ) * 100
        row = math.floor( xypos[1] / 100 ) * 100
        return (col,row)

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
        self.name = self.team + "Pawn" + self.position

    def fn_posible_moves( self ):
        pass

    def fn_possible_takes( self ):
        pass

    def fn_update_name( self ):
        self.name = self.team + "Pawn" + self.position