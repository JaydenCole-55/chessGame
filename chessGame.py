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
screen=pygame.display.set_mode((width, height))
pygame.mixer.init()

# Initialize pathing
current_path = os.path.dirname(__file__)
resource_path = os.path.join(current_path, 'resources2')
image_path = os.path.join(resource_path, 'images')
audio_path = os.path.join(resource_path, 'audio')
pieces_img_path = os.path.join(image_path, "pieces")

# Load audio
pygame.mixer.music.load( os.path.join( audio_path, "intro.mp3" ) )
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Load images
start_button = pygame.image.load( os.path.join( image_path, "start button.png"))
quit_button  = pygame.image.load( os.path.join( image_path, "quit button.jpg"))
white_tile   = pygame.image.load( os.path.join( image_path, "white_square.jpg"))
black_tile   = pygame.image.load( os.path.join( image_path, "black_square.jpg"))

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

# Start main menu
main_menu = 0
while main_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(pos):
                main_menu = 0
                play = 1
            if quit_button_rect.collidepoint(pos):
                sys.exit()

    # Clear screen before drawing it again
    screen.fill(0)

    start_button_rect = screen.blit(start_button, ( int(width/2-128), int(height/2-200) ))
    quit_button_rect  = screen.blit(quit_button,  ( int(width/2-128), int(height/2+56)  ))

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
for pawnNum in range(16):
    if pawnNum < 8:
        team = 'W'
        img = WPawnImg
        row = '2'
    else:
        team = 'B'
        img = BPawnImg
        row = '7'
    
    pos = str(col[pawnNum % 8]) + str(row)
    pawn = Pawn(team, pos, img)  
    pieces = pieces + [pawn]

# Pieces are ready, start game
turn_num = -1
while 1:
    # Clear Screen
    screen.fill(0)

    # Determine which player turn
    if turn_num%2 == 0:
        player = 'W'
    else:
        player = 'B'
    
    # Draw the board
    for x in range(math.floor( width/ black_tile.get_width() ) + 6):
        for y in range( math.floor( height/ black_tile.get_height() ) + 6):
            if (x+y)%2 == 0:
                screen.blit(white_tile,(x*100,y*100))
            else:
                screen.blit(black_tile,(x*100,y*100))

    # First time through loop only draw the pieces, no turns
    turn_going = True
    if turn_num < 0:
        turn_going = False

    # Wait for user to choose where to move piece
    piece_chosen = 0  
    while turn_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if piece_chosen == 1:
                    chosen_piece.rect.center = pos
                    chosen_piece.fn_update_position(pos)
                    pieces.append(chosen_piece)
                    turn_going = False
                else:
                    for piece in pieces:
                        if piece.rect.collidepoint(pos):
                            # Player is attempting to move this piece
                            if piece.team == player:
                                # It's their piece
                                # Move piece with cursor
                                piece_chosen = 1
                                chosen_piece = pieces.pop( pieces.index( piece ) )
                                break
    
    # Check its a possible move and not outside/around the board
    # Check if it takes any piece
    # Check if it puts their king in danger
    # Check if it puts the other king in danger
    # End turn, switch turns

    # Draw the pieces
    for piece2 in pieces:
        piece2.rect = screen.blit(piece2.image,piece2.screenPos)
        print("I am a " + piece2.name + " located at: " + piece2.position + ". x = " + str(piece2.screenPos[0]) + ", y = " + str(piece2.screenPos[1]) )

    print("\n=======================\n")
    pygame.display.flip()
    turn_num = turn_num + 1