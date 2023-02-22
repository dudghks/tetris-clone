import pygame

screen = pygame.display.set_mode((1366, 768))

# 0: I, 1: J, 2: L, 3: O, 4: S, 5: T, 6: Z
START_PIECES = {
   0:[['_', '_', '_', '_', '_'],
      ['_', '_', '_', '_', '_'],
      ['_', 'I', 'I', 'I', 'I'],
      ['_', '_', '_', '_', '_'],
      ['_', '_', '_', '_', '_']],
   1:[['J', '_', '_'],
      ['J', 'J', 'J'],
      ['_', '_', '_']],
   2:[['_', '_', 'L'],
      ['L', 'L', 'L'],
      ['_', '_', '_']],
   3:[['_', 'O', 'O'],
      ['_', 'O', 'O'],
      ['_', '_', '_']],
   4:[['_', 'S', 'S'],
      ['S', 'S', '_'],
      ['_', '_', '_']],
   5:[['_', 'T', '_'],
      ['T', 'T', 'T'],
      ['_', '_', '_']],
   6:[['Z', 'Z', '_'],
      ['_', 'Z', 'Z'],
      ['_', '_', '_']]
}

# 0: I, 1: J, 2: L, 3: O, 4: S, 5: T, 6: Z
OFFSET_BOOK = {
   0:(((0, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)))
   1:[['J', '_', '_'],
      ['J', 'J', 'J'],
      ['_', '_', '_']],
   2:[['_', '_', 'L'],
      ['L', 'L', 'L'],
      ['_', '_', '_']],
   3:[['_', 'O', 'O'],
      ['_', 'O', 'O'],
      ['_', '_', '_']],
   4:[['_', 'S', 'S'],
      ['S', 'S', '_'],
      ['_', '_', '_']],
   5:[['_', 'T', '_'],
      ['T', 'T', 'T'],
      ['_', '_', '_']],
   6:[['Z', 'Z', '_'],
      ['_', 'Z', 'Z'],
      ['_', '_', '_']]
}

class Piece:
   shape = []
   piece_type = 0
   xpos = 0
   ypos = 0
   rot = 0
   def __init__(self, xpos, ypos, rot, piece_type):
      self.xpos = xpos
      self.ypos = ypos
      self.rot = rot
      self.piece_type = piece_type
      self.shape = START_PIECES.get(piece_type)
      # self.temp = None
   
   # Check for collision of a piece and an input grid
   def check_collision(self, input_grid):
      for i in range(len(input_grid)):
         for j in range(len(i)):
            # if a filled block in the shape array (not '_')
            # is in the same location as one in the input grid
            if self.shape[i][j] != '_' and input_grid[i][j] != '_':
               return True
      # If no collision is found, return false
      return False

   def rotate_left(self):
      # (y, -x). rows become columns. invert new columns
      return [[j[i] for j in self.shape] for i in range(len(self.shape))][::-1]

   def rotate_right(self):
      # (-y, x). rows become columns. invert new rows
      return [[j[i] for j in self.shape][::-1] for i in range(len(self.shape))]

class Field:
   game_grid = [['_' for x in range(10)] for x in range(22)]

   def __init__(self, game_grid):
      self.game_grid = game_grid

# Testing rotation
# test_piece = Piece(0, 0, 0, 5)
# for i in test_piece.shape:
#    print(i)
# print('========')
# for i in test_piece.rotate_right():
#    print(i)
# print('========')
# for i in test_piece.rotate_left():
#    print(i)