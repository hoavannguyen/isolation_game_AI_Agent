import random

CHECKMATE = 999

def findRandomMove(validMoves,blocked_list,enemy_square,poormove):
    validMoves = [move for move in validMoves if [move.endRow, move.endCol] not in blocked_list+ poormove]
    for move in validMoves:
        if [move.endRow,move.endCol] == enemy_square:
            return move
    if len(validMoves)== 0:
        return None
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove(gs, validMoves,blocked_squares,poor_moves):
    validMoves = [move for move in validMoves if [move.endRow, move.endCol] not in blocked_squares + poor_moves]
    maxScore = -CHECKMATE
    bestMove = None
    score = None
    for playerMove in validMoves:
        turnMultiplier_1 = 1 if gs.whiteToMove else -1
        gs.makeMove(playerMove)
        blocked_squares.append(gs.getBlockedSquare()[1])
        checkmate = [move for move in gs.getValidMoves() if [move.endRow, move.endCol] not in blocked_squares]
        if len(checkmate) ==0:
            score = CHECKMATE
        else:
            # Get AI valid move and Max valid moves
            r , c = playerMove.endRow,playerMove.endCol
            moves = getKnightmove(r,c,blocked_squares)

            # Get enemy valid move and Min valid moves
            rw,cw = get_white_location(gs.board)
            white_moves = [move for move in getKnightmove(rw,cw,blocked_squares) if move not in moves]
            enemyvalidmoves = [move for move in gs.getValidMoves() if [move.endRow, move.endCol] not in blocked_squares ]
            for enemymove in enemyvalidmoves:
                score = len(moves) * -turnMultiplier_1 + turnMultiplier_1 * len(white_moves)

                turnMultiplier_2 = 1 if gs.whiteToMove else -1
                gs.makeMove(enemymove)
                blocked_squares.append(gs.getBlockedSquare()[0])
                checkmate_2 = [move for move in gs.getValidMoves() if [move.endRow, move.endCol] not in blocked_squares] # Valid move of AI
                if len(enemyvalidmoves)==1 and [enemymove.endRow, enemymove.endCol] in [[move.endRow, move.endCol] for move in gs.getValidMoves()]:
                    score = CHECKMATE
                else:
                    score = score + turnMultiplier_2 * len(checkmate_2)

                if score > maxScore:
                    maxScore = score
                    bestMove = playerMove
                gs.undoMove()
                blocked_squares.pop()
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
        blocked_squares.pop()
    return  bestMove
def findMove_Medium(gs, validMoves,blocked_squares,poor_moves):
    validMoves = [move for move in validMoves if [move.endRow, move.endCol] not in blocked_squares + poor_moves]
    maxScore = -CHECKMATE
    bestMove = None
    score = None
    for playerMove in validMoves:
        turnMultiplier_1 = 1 if gs.whiteToMove else -1
        gs.makeMove(playerMove)
        blocked_squares.append(gs.getBlockedSquare()[1])
        checkmate = [move for move in gs.getValidMoves() if [move.endRow, move.endCol] not in blocked_squares]
        if len(checkmate) == 0:
            score = CHECKMATE
        else:
            # Get AI valid move and Max valid moves
            r , c = playerMove.endRow,playerMove.endCol
            moves = getKnightmove(r,c,blocked_squares)
            score = len(moves) * -turnMultiplier_1

            # Get enemy valid move and Min valid moves
            rw,cw = get_white_location(gs.board)
            white_moves = [move for move in getKnightmove(rw,cw,blocked_squares) if move not in moves]
            score += turnMultiplier_1 * len(white_moves)

        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
        blocked_squares.pop()
    return bestMove
def getKnightmove(r,c,blocked_sq):
    knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    moves = []
    for m in knightMoves:
        endRow = r + m[0]
        endCol = c + m[1]
        if 0 <= endRow < 7 and 0 <= endCol < 7 and [endRow, endCol] not in blocked_sq:
            moves.append([endRow, endCol])
    return moves
def get_white_location(board):
    location = None
    for r in range(len(board)):
        for c in range(len(board[r])):
            turn = board[r][c][0]
            if turn == 'w':
                location = [r, c]
    return location
def get_black_location(board):
    location = None
    for r in range(len(board)):
        for c in range(len(board[r])):
            turn = board[r][c][0]
            if turn == 'b':
                location = [r, c]
    return location