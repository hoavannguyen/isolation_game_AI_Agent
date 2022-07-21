class GameState():
    def __init__(self):
        #board 8x8, 2d array
        #2 character bK= black knight ; wK= white knight
        # "--" is emty space
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
        ]
        self.moveFunctions = { 'K':self.getKnightMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.white_blocked_square = None
        self.white_blocked_square = None

    def first_turn(self,r,c):
        if self.whiteToMove:
            self.board[r][c] = 'wK'
            self.whiteToMove = not self.whiteToMove
        else:
            self.board[r][c] = 'bK'
            self.whiteToMove = not self.whiteToMove

    def makeMove(self,move):
        """Not work for castling, pawn promotion, en-passant in chess"""
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn =='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove) :
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    def getBlockedSquare(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if turn == 'w':
                    self.white_blocked_square = [r,c]
                if turn =='b':
                    self.black_blocked_square = [r,c]
        return [self.white_blocked_square,self.black_blocked_square]
    def getKnightMoves(self,r,c,moves):
        knightMoves =((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow < 7 and 0 <= endCol <7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
class Move():
    rankstoRows = {
        "1":6,"2":5,"3":4,"4":3,
        "5":2,"6":1,"7":0
    }
    rowstoRanks = {v:k for k,v in rankstoRows.items()}
    filestoCols= {
        "a":0,"b":1,"c":2,"d":3,
        "e":4,"f":5,"g":6
    }
    colstoFiles = {v:k for k,v in filestoCols.items()}
    def __init__(self,startSQ, endSQ,board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 +self.startCol*100 + self.endRow*10 +self.endCol
        #print(self.moveID)
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    def getChessNotaion(self):

        return self.getRankFile(self.startRow,self.startCol)+ self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colstoFiles[c]+self.rowstoRanks[r]