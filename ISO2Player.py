import pygame as p
import ISOEngine
import ISOMain
BOARD_WIDTH = BOARD_HEIGHT = 668
GAME_STATUS_WIDTH = 252
GAME_STATUS_HEIGHT = BOARD_HEIGHT

DIMENSION = 7 # chess board 8x8
SQ_SIZE = BOARD_HEIGHT//DIMENSION # Square size
MAX_FPS=60
IMAGES = {}
"""
Initialize a global dictionary of images. Once in the main
"""
def loadImages():
    pieces = ['wK',"bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Images/'+piece+'.png'),(SQ_SIZE,SQ_SIZE))
"""
The main driver. Will handle user input and update the graphics
"""
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + GAME_STATUS_WIDTH,BOARD_HEIGHT))
    p.display.set_caption("ISOLATION GAME")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ISOEngine.GameState()

    blocked_squares = []
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False # flag variable

    #loadImages() # only do this once
    running = True
    sqSelected = ()
    playerClicks = []
    turn_count = 0
    w_score = 0
    b_score = 0

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                import sys
                sys.exit('Bye')
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) lct of mouse
                if 9 * SQ_SIZE < location[0] < 9 * SQ_SIZE + SQ_SIZE/ 2 and 20< location[1] < 20 + SQ_SIZE / 2:
                    ISOMain.main()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if turn_count < 2 and col < 7:
                    gs.first_turn(row,col)
                    loadImages()
                    validMoves = gs.getValidMoves()
                    turn_count +=1
                else:
                    if sqSelected == (row,col) or col >=7:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected) # 1st and 2nd click
                    if len(playerClicks)==2:
                        blocking = gs.getBlockedSquare()
                        move = ISOEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotaion())
                        if move in validMoves and [move.endRow,move.endCol] not in blocked_squares:
                            gs.makeMove(move)
                            if not gs.whiteToMove:
                                blocked_squares.append(blocking[0])
                            else:
                                blocked_squares.append(blocking[1])
                            moveMade = True
                            animate = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen,gs, validMoves,sqSelected,blocked_squares)

        if turn_count == 2:
            checkmate = [[move.endRow,move.endCol] for move in gs.getValidMoves()]
            checking = [ i for i in checkmate if i not in blocked_squares]
            if len(checking)== 0:
                if gs.whiteToMove:
                    drawText(screen,'Black WIN! Congratulations!')
                else:
                    drawText(screen, 'White WIN! Congratulations!')
                # Restart button
                play_button = p.transform.scale(p.image.load('Images/play_button.png'), (SQ_SIZE*2, SQ_SIZE*2))
                screen.blit(play_button, p.Rect(2.5*SQ_SIZE,2.3*SQ_SIZE,SQ_SIZE*2,SQ_SIZE*2))
                for event in p.event.get():
                    if event.type == p.QUIT:  # Nút tắt
                        running = False
                    if event.type==p.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = p.mouse.get_pos()
                        if 2.5 * SQ_SIZE <mouse_y<2.5 * SQ_SIZE+ SQ_SIZE *2 and 2.3*SQ_SIZE <mouse_x< 2.3*SQ_SIZE + SQ_SIZE*2:
                            blocked_squares = []
                            validMoves = gs.getValidMoves()
                            moveMade = False
                            animate = False
                            sqSelected = ()
                            playerClicks = []
                            gs.board = [
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                    ["--", "--", "--", "--", "--", "--", "--"],
                                ]
                            turn_count = 0
                        if 9 * SQ_SIZE < mouse_x< 9 * SQ_SIZE + SQ_SIZE / 2 and 20 < mouse_y < 20 + SQ_SIZE / 2:
                            ISOMain.main()
        clock.tick(MAX_FPS)
        p.display.flip()

def drawPlayerTurn(screen, gs):
    PlayerTurnRect = p.Rect(BOARD_WIDTH,0,GAME_STATUS_WIDTH,GAME_STATUS_HEIGHT)
    p.draw.rect(screen,p.Color(175, 149, 222),PlayerTurnRect)
    padding=12
    font = p.font.SysFont('Arial',39,True,False)
    text = 'White' if gs.whiteToMove else 'Black'
    textObject1 = font.render('Player Turn:', True, p.Color(55, 92, 0))
    textObject2 = font.render(text, True, p.Color(55, 92, 0))
    textLocation1 = PlayerTurnRect.move(padding,69)
    textLocation2 = PlayerTurnRect.move(padding,112)
    screen.blit(textObject1,textLocation1)
    screen.blit(textObject2,textLocation2)
    #Home Button
    home_button = p.transform.scale(p.image.load('Images/home.png'), (SQ_SIZE/2, SQ_SIZE/2))
    screen.blit(home_button, p.Rect(9 * SQ_SIZE, 20, SQ_SIZE/2, SQ_SIZE/2))


def drawText(screen,text):
    font = p.font.SysFont('Verdana',39,True,False)
    textObject = font.render(text,0,p.Color('Black'))
    textLocation = p.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT).move(BOARD_WIDTH/1.3 - textObject.get_width()/1.3,BOARD_HEIGHT/1.3 -textObject.get_height()/1.3)
    screen.blit(textObject,textLocation)
def drawBlockedSquare(screen,blocked_list):
    for i in range(len(blocked_list)):
        r,c = blocked_list[i]
        if i %2 ==0:
            p.draw.rect(screen,p.Color(82, 83, 92),p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            p.draw.line(screen,p.Color(171, 169, 156),(c*SQ_SIZE,r*SQ_SIZE),(c*SQ_SIZE+SQ_SIZE,r*SQ_SIZE+SQ_SIZE))
            p.draw.line(screen,p.Color(171, 169, 156),(c*SQ_SIZE+SQ_SIZE,r*SQ_SIZE),(c*SQ_SIZE,r*SQ_SIZE+SQ_SIZE))
        else:
            p.draw.rect(screen, p.Color(21, 32, 94), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.draw.line(screen,p.Color(234, 220, 202),(c*SQ_SIZE,r*SQ_SIZE),(c*SQ_SIZE+SQ_SIZE,r*SQ_SIZE+SQ_SIZE))
            p.draw.line(screen,p.Color(234, 220, 202),(c*SQ_SIZE+SQ_SIZE,r*SQ_SIZE),(c*SQ_SIZE,r*SQ_SIZE+SQ_SIZE))


def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r , c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #highlight selected square
            s= p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transparent
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE,r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color(5, 252, 248))
            for move in validMoves :
                if move.startRow == r and move.startCol ==c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))

def drawGameState(screen,gs,validMoves,sqSelected,blocked_list):
    drawBoard(screen) # draw squares on the board
    drawPlayerTurn(screen,gs)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawBlockedSquare(screen,blocked_list)
    drawPieces(screen,gs.board) # draw pieces

def drawBoard(screen):
    global colors
    colors = [p.Color(235,235,208),p.Color(119,148,85)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column)%2)] # Ô CÓ HÀNG+CỘT CHẴN THÌ MÀU TRẮNG VÀ NGƯỢC LẠI
            p.draw.rect(screen,color,p.Rect(column*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # frames to move square
    frameCount = (abs(dR)+abs(dC)) *framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startRow + dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece move
        color = colors[(move.endRow + move.endCol) %2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
if __name__== "__main__":
    main()