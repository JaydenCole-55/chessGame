# 1 - Import library
import pygame
from pygame.locals import *
import math
import os
import sys
import math
from chessClass import *

# Initialize the screen
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode( ( width, height ) )
pygame.mixer.init()

# Initialize pathing
current_path    = os.path.dirname( __file__ )
resource_path   = os.path.join( current_path,  'resources2' )
image_path      = os.path.join( resource_path, 'images'     )
audio_path      = os.path.join( resource_path, 'audio'      )
pieces_img_path = os.path.join( image_path,    'pieces'     )
log_path        = os.path.join( current_path,  'game log'   )

# Load audio
pygame.mixer.music.load( os.path.join( audio_path, "intro.mp3" ) )
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Load images
start_button = pygame.image.load( os.path.join( image_path, "start button.png"))
quit_button  = pygame.image.load( os.path.join( image_path, "quit button.jpg"))
white_tile   = pygame.image.load( os.path.join( image_path, "white_square.jpg"))
black_tile   = pygame.image.load( os.path.join( image_path, "black_square.jpg"))
red_dot      = pygame.image.load( os.path.join( image_path, "red_dot2.jpg"))

# Load images for the pieces
WKingImg   = pygame.image.load( os.path.join( pieces_img_path, "WKing.png"))
WQueenImg  = pygame.image.load( os.path.join( pieces_img_path, "WQueen.png"))
WRookImg   = pygame.image.load( os.path.join( pieces_img_path, "WRook.png"))
WKnightImg = pygame.image.load( os.path.join( pieces_img_path, "WKnight.png"))
WBishopImg = pygame.image.load( os.path.join( pieces_img_path, "WBishop.png"))
WPawnImg   = pygame.image.load( os.path.join( pieces_img_path, "WPawn.png"))
BKingImg   = pygame.image.load( os.path.join( pieces_img_path, "BKing.png"))
BQueenImg  = pygame.image.load( os.path.join( pieces_img_path, "BQueen.png"))
BRookImg   = pygame.image.load( os.path.join( pieces_img_path, "BRook.png"))
BKnightImg = pygame.image.load( os.path.join( pieces_img_path, "BKnight.png"))
BBishopImg = pygame.image.load( os.path.join( pieces_img_path, "BBishop.png"))
BPawnImg   = pygame.image.load( os.path.join( pieces_img_path, "BPawn.png"))

# Open file to log moves
log_file = os.path.join( log_path, "Game Log.txt" )
gameFile = open( log_file, "w" )

def main():
    # Start main menu
    main_menu = 0
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint( pos ):
                    main_menu = 0
                    play = 1
                if quit_button_rect.collidepoint( pos ):
                    sys.exit()

        # Clear screen before drawing it again
        screen.fill(0)

        start_button_rect = screen.blit( start_button, ( int(width/2-128), int(height/2-200 ) ) )
        quit_button_rect  = screen.blit( quit_button,  ( int(width/2-128), int(height/2+56  ) ) )

        pygame.display.flip()

    # Get Game Ready
    # Initialize pieces
    WKing    = King   ( 'W', 'e1', WKingImg   )
    WQueen   = Queen  ( 'W', 'd1', WQueenImg  )
    WRook1   = Rook   ( 'W', 'a1', WRookImg   )
    WRook2   = Rook   ( 'W', 'h1', WRookImg   )
    WKnight1 = Knight ( 'W', 'b1', WKnightImg )
    WKnight2 = Knight ( 'W', 'g1', WKnightImg )
    WBishop1 = Bishop ( 'W', 'c1', WBishopImg )
    WBishop2 = Bishop ( 'W', 'f1', WBishopImg )

    BKing    = King   ( 'B', 'e8', BKingImg   )
    BQueen   = Queen  ( 'B', 'd8', BQueenImg  )
    BRook1   = Rook   ( 'B', 'a8', BRookImg   )
    BRook2   = Rook   ( 'B', 'h8', BRookImg   )
    BKnight1 = Knight ( 'B', 'b8', BKnightImg )
    BKnight2 = Knight ( 'B', 'g8', BKnightImg )
    BBishop1 = Bishop ( 'B', 'c8', BBishopImg )
    BBishop2 = Bishop ( 'B', 'f8', BBishopImg )

    # Consolidate the pieces
    pieces = [ WKing, WQueen, WRook1, WRook2, WKnight1, WKnight2, WBishop1, WBishop2 ]
    pieces = pieces + [ BKing, BQueen, BRook1, BRook2, BKnight1, BKnight2, BBishop1, BBishop2 ]

    # Create the pawns
    col = { 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h' }
    for pawnNum in range( 16 ):
        if pawnNum < 8:
            team = 'W'
            img = WPawnImg
            row = '2'
        else:
            team = 'B'
            img = BPawnImg
            row = '7'

        pos = str( col[pawnNum % 8] ) + str( row )
        pawn = Pawn(team, pos, img)
        pieces = pieces + [pawn]

    # Pieces are ready, start game
    turn_num = -1 # Turn -1 initializes board
    while 1:
        # Clear Screen
        screen.fill(0)

        # Determine which player turn
        if turn_num%2 == 0:
            player = 'W'
            print("White turn")
        else:
            player = 'B'
            print("Black turn")

        # First time through loop only draw the pieces, no turns
        turnGoing = True
        if turn_num < 0:
            turnGoing = False

        # Wait for user to choose where to move piece
        chosenPiece = None
        oldPos = None
        while turnGoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    gameFile.close()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:   
                    pos = pygame.mouse.get_pos()

                    if chosenPiece != None:
                        # A piece has been chosen
                        newPos = fn_get_square( pos )

                        if newPos == oldPos:
                            # User clicked on the same piece twice, deselect piece and don't move it
                            [pieces, chosenPiece, oldPos] = fn_deselect_piece( piece, pieces, chosenPiece, oldPos )
                            fn_draw_board( screen, black_tile, pieces, [], pygame.display)
                            continue

                        # Check if it is a possible move
                        possibleSquareNums = chosenPiece.fn_possible_moves( pieces )

                        if newPos not in possibleSquareNums:
                            # Where the player clicked is not a good move, make them click a good move
                            print("Not a valid move")
                            continue

                        # Check if its a castle
                        castles = ""
                        if "King" in piece.name:
                            if piece.team == 'W' and not piece.hasMoved and newPos == 7:
                                # This is a white king side castles situation, move the rook as well
                                fn_move_piece( 8, 6, pieces)
                                castles = "0-0 "
                            elif piece.team == 'W' and not piece.hasMoved and newPos == 3:
                                # This is a white queen side castles situation, move the rook as well
                                fn_move_piece( 1, 4, pieces)
                                castles = "0-0-0 "
                            elif piece.team == 'B' and not piece.hasMoved and newPos == 63:
                                # This is a black king side castles situation, move the rook as well
                                fn_move_piece( 64, 62, pieces)
                                castles = "0-0"
                            elif piece.team == 'B' and not piece.hasMoved and newPos == 59:
                                # This is a black queen side castles situation, move the rook as well
                                fn_move_piece( 57, 60, pieces)
                                castles = "0-0-0"

                        # Check if it takes an opponents piece
                        takes = fn_check_if_takes( pos, pieces, player )

                        # Then move piece to that position and append it back to pieces
                        chosenPiece.rect.center = pos
                        chosenPiece.fn_update_position( pos )

                        # Write the move to the game log
                        fn_write_to_game_log( player, chosenPiece, takes, castles )

                        # If King/rook move means no more castling with that piece
                        if "King" in piece.name or "Rook" in piece.name:
                            chosenPiece.hasMoved = True

                        pieces.append( chosenPiece )

                        # End the turn
                        turnGoing = False
                    else:
                        for piece in pieces:
                            if piece.rect.collidepoint( pos ) and piece.team == player:
                                # Player is attempting to move this piece
                                # Remove from pieces list to be modified and appended back later

                                # Check if the piece can move
                                possibleSquares = piece.fn_possible_moves( pieces )
                                if not possibleSquares:
                                    # This piece has no moves, player cannot select this piece
                                    print("This piece has no moves")
                                else:
                                    # Draw the possible move to the screen
                                    fn_draw_board( screen, black_tile, pieces, possibleSquares, pygame.display)

                                chosenPiece = pieces.pop( pieces.index( piece ) )
                                oldPos = fn_get_square( pos )
                                break

                # Right click to deselect piece
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    [pieces, chosenPiece, oldPos] = fn_deselect_piece( piece, pieces, chosenPiece, oldPos )
                    fn_draw_board( screen, black_tile, pieces, [], pygame.display)

        # Check if it puts their king in danger
        # Check if it puts the other king in danger
        # End turn, switch turns

        # Draw the board
        fn_draw_board( screen, black_tile, pieces, [], pygame.display )

        turn_num = turn_num + 1


def fn_check_if_takes( pos, pieces, player ):
    # Passed: cords of the position, list of pieces, the player colour
    # Returns: bool
    # Checks if the passed square has an oppenent piece and removes it
    for piece in pieces:
        if piece.rect.collidepoint(pos):
            if piece.team != player:
                pieces.pop( pieces.index( piece ) )
                return True

    return False


def fn_get_square( position ):
    # Passed: a tuple of Coordinates
    # Returns: the square number
    x = position[0]
    y = position[1]
    return 64 - 8 * (math.floor( y/100 ) + 1) + math.floor( x/100 ) + 1


def fn_get_screen_coords( sqNum ):
    # Passed: a square number
    # Returns: a tuple of coordinates
    x = ( ( sqNum % 8 ) - 1) * 100
    if x < 0:
        x = 700
    y = ( 8 - math.ceil( sqNum / 8 ) ) * 100
    return (x, y)


def fn_move_piece( position1, position2, pieces ):
    # Passed: int, int, list
    # Returns: None
    # Moves piece at position1 to position2
    for piece in pieces:
        if piece.squareNum == position1:
            piece.fn_update_position( position2 )


def fn_write_to_game_log( player, chosenPiece, takes, castles ):
    # Passed: String, Piece, bool, bool
    # Returns: None
    # Writes to game log what move was played
    
    if takes:
        gameFile.write( chosenPiece.abbrv + 'x' + chosenPiece.chessPosition + ' ' )
    elif castles:
        gameFile.write( castles )
    else:
        gameFile.write( chosenPiece.abbrv + chosenPiece.chessPosition + ' ' )

    if player == 'B':
        gameFile.write( '\n' )


def fn_draw_tiles( screen, tiles ):
    # Passed: Screen object, tile picture
    # Returns: None
    # Draws the background screen
    for x in range(math.floor( width/ tiles.get_width() ) + 6):
        for y in range( math.floor( height/ tiles.get_height() ) + 6):
            if( x + y ) % 2 == 0:
                screen.blit( white_tile, ( x * 100, y * 100 ) )
            else:
                screen.blit( black_tile, ( x * 100, y * 100 ) )


def fn_draw_pieces( screen, pieces ):
    for piece in pieces:
        piece.rect = screen.blit( piece.image, piece.screenPosition )


def fn_draw_possible_moves( screen, possible_moves ):
    # Passed: A screen, list
    # Returns: None
    # Draws red dots to possible move points
    for move in possible_moves:
        x,y = fn_get_screen_coords( move )
        # Move the dot to the centre
        screenCoords = (x+40, y+40)
        screen.blit( red_dot, screenCoords )


def fn_draw_board( screen, tiles, pieces, possible_moves, display ):
    fn_draw_tiles ( screen, tiles )
    fn_draw_pieces( screen, pieces )
    fn_draw_possible_moves( screen, possible_moves )

    display.flip()


def fn_deselect_piece( piece, pieces, chosenPiece, oldPos ):
    # Passed: A piece, the pieces
    # Return: None
    pieces.append( piece )
    chosenPiece = None
    oldPos      = None
    return [pieces, chosenPiece, oldPos]


if __name__ == "__main__":
    main()
    gameFile.close()
    