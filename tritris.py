#!/usr/bin/env python

import pygame, os, random, pygame.draw as draw
from pygame.locals import *

import piece, board
Piece = piece.Piece
Board = board.Board
from gameSettings import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required" )
    
controls = {}
for key in ['up', 'down', 'left', 'right', 'a', 'b', 'x', 'y']:
    controls[key] = False
keysToControls = {
    K_UP: 'up',
    K_DOWN: 'down',
    K_LEFT: 'left',
    K_RIGHT: 'right',
    K_w: 'up',
    K_s: 'down',
    K_a: 'left',
    K_d: 'right',
    K_SPACE: 'a'
}

def processControls():
    #get input  
    for event in pygame.event.get():
        if event.type == QUIT:
            return "quit"
        #game buttons
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "quit"
            elif event.key in keysToControls:
                controls[keysToControls[event.key]] = True
        elif event.type == KEYUP:
            if event.key in keysToControls:
                controls[keysToControls[event.key]] = False
        #demo buttons
        if event.type == KEYDOWN and doDemo:
            return "clock"

def main():
    gameWindow = Rect( 0, 0, 800, 704 )
    clock = pygame.time.Clock()

    main_dir = os.path.split( os.path.abspath( __file__ ) )[0]
    
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ( 'Warning, no sound' )
        pygame.mixer = None    
    pygame.display.set_caption( 'Tritris v0.1' )
    
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok( gameWindow.size, winstyle, 32 )
    screen = pygame.display.set_mode( gameWindow.size, winstyle, bestdepth )
    
    board = pygame.Surface( (128 * 3, 192 * 3), pygame.SRCALPHA )    
    boardCorner = (24 * 16, 64) 
    boardX, boardY = boardCorner
    global doDemo
    
    if doDemo:
        #instantiate demo pieces
        demoPieces = [None]*8
        for i in range(0, 8):
            demoPieces[i] = Piece( i + 1, (i % 4 ) * 2, int( i/4 ) * 2, colors[i] )
    demoClockwise = True
    ticks = -1
    
    quitGame = False
    
    while not quitGame:
        controlsReturnVal = processControls()
        if controlsReturnVal == "quit":
            quitGame = True
            print( 'quittin\'' )
        elif controlsReturnVal == "clock":
            demoClockwise = not demoClockwise    
            
        screen.fill( Color(0,0,0) )
        board.fill( Color(0,0,0,0) )
        
        ticks += 1     
        
        if demoGrids:
            for x in range(1, int( gameWindow.w/16 ) + 1):
                draw.line( screen, cGrid, (x * 16, 0), (x * 16, gameWindow.h) )
            for y in range(1, int( gameWindow.h/16 ) + 1):
                draw.line( screen, cGrid, (0, y * 16), (gameWindow.w, y * 16) )
        draw.rect( screen, cGameBG, (boardCorner,(128 * 3, 192 * 3)) )
        
        for x in range( 1, 8 ):
            draw.line( screen, cGameGrid, (boardX + x * 48, boardY), (boardX + x * 48, boardY +48 * 12) )
        for y in range( 1, 12 ):
            draw.line( screen, cGameGrid, (boardX, boardY + y * 48), (boardX + 48 * 8, boardY + y * 48) )
           
        if demoPieces:
            if ticks == 30:
                for i in range(0, 8):
                    demoPieces[i].rotate( demoClockwise )
                ticks = 0
            
            for i in range(0, 8):
                demoPieces[i].draw( board )
        else:
            pass
        
        screen.blit( board, boardCorner )
        
        pygame.display.update()
        #cap the framerate
        clock.tick(60)

    pygame.quit()

 
#call the "main" function if running this script
if __name__ == '__main__': main()