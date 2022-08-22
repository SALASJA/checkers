import math
from copy import deepcopy

#PIECE CONSTANTS
SPACE = 0
WHITE = 1
RED = 2
WHITEKING = 3
REDKING = 4

#ACTION CONSTANTS
ISILLEGAL = 0
ISPIECE = 1
ISFORCEJUMPPIECE = 2
ISJUMP = 3
ISMOVE = 4


class Checkers:
	def __init__(self):
		self.board = [[0,2,0,2,0,2,0,2],
					  [2,0,2,0,2,0,2,0],
					  [0,2,0,2,0,2,0,2],
					  [0,0,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0]]
					  
		self.actionMap = [[0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					      [0,0,0,0,0,0,0,0],
					      [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
						  [0,0,0,0,0,0,0,0]]
						  

		self.previousPiece = None;
		
		self.turn = True; #when True its whites turn
		self.multijump = False;
		self.numRedPieces = 12;
		self.numWhitePieces = 12;
		self.selectedPiece = None;
		self.generateMap();

	def reset(self):
		self.board = [[0,2,0,2,0,2,0,2],
					  [2,0,2,0,2,0,2,0],
					  [0,2,0,2,0,2,0,2],
					  [0,0,0,0,0,0,0,0],
					  [0,0,0,0,0,0,0,0],
					  [1,0,1,0,1,0,1,0],
					  [0,1,0,1,0,1,0,1],
					  [1,0,1,0,1,0,1,0]]
					  
		self.actionMap = [[0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					      [0,0,0,0,0,0,0,0],
					      [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
					  	  [0,0,0,0,0,0,0,0],
						  [0,0,0,0,0,0,0,0]]
		self.previousPiece = None;
		
		self.turn = True; #when True its whites turn
		self.multijump = False;
		self.numRedPieces = 12;
		self.numWhitePieces = 12;
		self.selectedPiece = None;
		self.generateMap();
	
	def getWinningPiece(self):
		if self.numRedPieces > 0 and self.numWhitePieces > 0:
			return 0
			
		i = self.previousPiece[0]
		j = self.previousPiece[1]
		piece_type = self.board[i][j]
		if piece_type in [WHITE, WHITEKING]:
			return WHITE;
		
		return RED
	
	def gameOver(self):
		result = self.getWinningPiece()
		return result != 0
	
	def isValidMatrixPosition(self, i,j):
		return i != None and j != None and 0 <= i and i < len(self.board) and 0 <= j and j < len(self.board[i]) 
		
	
	def isValidMove(self,i,j):
		
		piece_i = self.selectedPiece[0]
		piece_j = self.selectedPiece[1]
		
		if i == piece_i or piece_j == j:
			return False
		
		distance = math.sqrt((piece_i - i)**2 + (piece_j - j) ** 2)
		
		if distance > math.sqrt(8):
			return False
		
		
		piece_type = self.board[piece_i][piece_j]

		
		
		direction = i - piece_i; 
		
		
		if piece_type == WHITE and direction < 0:
			return True
		
		if piece_type == RED and direction > 0:
			return True
		
		if piece_type in [WHITEKING, REDKING]:
			return True
		
		return False
	
	def isJump(self, action_type):
		return action_type == ISJUMP
	
	def isPieceSelection(self, action_type):
		return action_type in [ISPIECE, ISFORCEJUMPPIECE]
	
	def isMove(self, action_type):
		return action_type == ISMOVE
	
	def isIllegal(self, action_type):
		return action_type == ISILLEGAL
	
	def pieceNotSelected(self):
		return self.selectedPiece == None
		
		
		
	def isValidSelection(self, i,j): 
		if not self.isValidMatrixPosition(i,j):
			return False
			
		action_type = self.actionMap[i][j]
		
		
		if self.isIllegal(action_type):
			return False
		
		if (self.isMove(action_type) or self.isJump(action_type)) and self.pieceNotSelected():
			return False
		
		if (self.isMove(action_type) or self.isJump(action_type)) and self.isValidMove(i,j):
			return True
		
		if self.isPieceSelection(action_type):
			return True
			
		return False 
		
	#end of selection methods
	
	def select(self, i,j):
		self.selectedPiece = [i,j]

	def move(self,i,j, is_jump = False):
		piece_i = self.selectedPiece[0]
		piece_j = self.selectedPiece[1]
		space_i = i
		space_j = j
		
		to_remove_i = (piece_i + space_i) // 2
		to_remove_j = (piece_j + space_j) // 2
		
		piece_type = self.board[piece_i][piece_j]
		
		if piece_type == RED and space_i == len(self.board) - 1:
			piece_type = REDKING
		
		if piece_type == WHITE and space_i == 0:
			piece_type = WHITEKING
			
		self.board[space_i][space_j] = piece_type
		self.board[piece_i][piece_j] = SPACE
		self.previousPiece = [space_i,space_j] 
		self.selectedPiece = None
		
		if is_jump:
			opponent_piece_type = self.board[to_remove_i][to_remove_j]
			self.board[to_remove_i][to_remove_j] = SPACE
			if opponent_piece_type in [WHITE,WHITEKING]: 
				self.numWhitePieces -= 1
			if opponent_piece_type in [RED,REDKING]: 
				self.numRedPieces -= 1
		
	
	def performSelection(self, i,j):
		action_type = self.actionMap[i][j]
		is_jump = self.isJump(action_type)
		if self.isMove(action_type) or is_jump:		
			self.move(i,j,is_jump)
			willjumpagain = self.generateMap()
			
			if is_jump and willjumpagain:
				self.multijump = True
				self.selectedPiece = self.previousPiece
				return
				
			self.multijump = False
			self.turn = not self.turn
			self.generateMap()
			
		elif self.isPieceSelection(action_type):
			self.select(i,j)
	
	#end of operation methods
	
	def resetMap(self):
		for i in range(len(self.actionMap)):
			for j in  range(len(self.actionMap[i])):
				self.actionMap[i][j] = ISILLEGAL
	
	def markPiece(self, i,j,piecejumps = False):
		self.actionMap[i][j] = ISFORCEJUMPPIECE if piecejumps else ISPIECE
	
	
	def getPossiblePositions(self, piece_type, i, j):
		possible_positions = { 0 : [i - 1, j - 1], 1 : [i - 1, j + 1], 2 : [i + 1, j - 1], 3 : [i + 1, j + 1]}
		if piece_type == WHITE:
			possible_positions = {0 : [i - 1, j - 1], 1 : [i - 1, j + 1]}
		
		if piece_type == RED:
	  		possible_positions = {2 : [i + 1, j - 1], 3 : [i + 1, j + 1]}
		return possible_positions
	
	def isSpace(self, i,j):
		if not self.isValidMatrixPosition(i,j):
			return False
		piece_type = self.board[i][j]
		return piece_type == SPACE
	
	def markMoveSpace(self, i,j):
		action_type = self.actionMap[i][j]
		if action_type in [ISFORCEJUMPPIECE, ISJUMP]:
			return
			
		self.actionMap[i][j] = ISMOVE
	
	
	def areOpposablePieces(self, piece_type1, piece_type2):
		if piece_type1 in [WHITE, WHITEKING] and piece_type2 in [RED, REDKING]:
			return True
		
		if piece_type2 in [WHITE, WHITEKING] and piece_type1 in [RED, REDKING]:
			return True
			
		return False
	
	def isJumpable(self, piece_type, i, j, corner_type):
		"""
		w/wk/rk,0 --> [i - 1, j - 1]    0
		w/wk/rk,1 --> [i - 1, j + 1]    1
		r/wk/rk,2 --> [i + 1, j - 1]    2
		r/wk/rk,3 --> [i + 1, j + 1]    3
		"""
		if not self.isValidMatrixPosition(i,j):
			return None
		
		opponent_piece_type = self.board[i][j]
		
		if not self.areOpposablePieces(piece_type, opponent_piece_type):
			return None
		
		positions_dict = self.getPossiblePositions(piece_type, i,j)
		
		possible_jump = positions_dict[corner_type]
		possible_i = possible_jump[0]
		possible_j = possible_jump[1]
		
		if not self.isSpace(possible_i, possible_j):
			return None
			
		return [possible_i, possible_j]
	
	def markJumpSpace(self, i,j, offset=0):
		action_type = self.actionMap[i][j]
		if action_type in [ISILLEGAL, ISMOVE]:
			self.actionMap[i][j] = ISJUMP

	
	def mapPieceMoves(self, i,j):
		willjump = False
		piece_type = self.board[i][j]
		positions_dict = self.getPossiblePositions(piece_type, i,j)
		
		for corner_type in positions_dict:
			possible_move = positions_dict[corner_type]
			possible_i = possible_move[0]
			possible_j = possible_move[1]
			if self.isSpace(possible_i, possible_j):
				self.markMoveSpace(possible_i, possible_j)
			else:
				jumpable = self.isJumpable(piece_type, possible_i, possible_j, corner_type)
				if jumpable != None:
					possible_jump_i = jumpable[0]
					possible_jump_j = jumpable[1]
					willjump = True
					self.markJumpSpace(possible_jump_i, possible_jump_j)
					
		return willjump
	
	
	def filterMap(self):
		for i in range(len(self.actionMap)):
			for j in range(len(self.actionMap[i])):
				action_type = self.actionMap[i][j]
				if action_type in [ISPIECE, ISMOVE]:
					self.actionMap[i][j] = ISILLEGAL
	
	def isValidPiece(self, i,j):
		piece_type = self.board[i][j]
		
		if self.turn:
			return piece_type in [WHITE,WHITEKING]
		
		return piece_type in [RED,REDKING] 
	
	def generateMap(self):
		self.resetMap()
		willjump = False
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.isValidPiece(i,j):
					piecejumps = self.mapPieceMoves(i,j)
					self.markPiece(i,j,piecejumps)
					willjump |= piecejumps
					
		if willjump:
			self.filterMap()
			
		return willjump
	
	
	
	def toString(self, boardmode=True):
		piece_chars = { SPACE : ' ', WHITE: 'w', RED : 'r', WHITEKING : 'W', REDKING : 'R'}
		result = "\n\n\n-----------------------------------------------------------------\n"
		for i in range(len(self.board)):
			result += "|"
			for j in range(len(self.board[i])):
				value = self.board[i][j] if boardmode else self.actionMap[i][j]
				character = piece_chars[value] if boardmode else self.actionMap[i][j]
				character = str(character)
				if len(character) == 1:
					character = ' ' + character + ' '
				elif len(character) == 2:
					character = ' ' + character
					
				result += f"  {character}  |"
			result += "\n-----------------------------------------------------------------\n"
		
		result += f"Selected: {self.selectedPiece}\n"
		result += "white's turn\n" if self.turn else "red's turn\n"
		return result
	
	def __str__(self):
		return self.toString()
		
	def getState(self):
		return {"selected": deepcopy(self.selectedPiece), 
				"locations": deepcopy(self.board),
				"turn": self.turn,
				"multijump": self.multijump,
				"winningpiece": self.getWinningPiece()}



def main():
	game = Checkers()
	while not game.gameOver():
		print(game)
		i = int(input("Enter a row: "))
		j = int(input("Enter a column: "))
		if game.isValidSelection(i,j):
			game.performSelection(i,j)
		else:
			print("Invalid Selection!")
		
			
if __name__ == "__main__":
	main()
		
		
		