import pygame
import random

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

# 0: I | 1: J, L, S, T, Z | 2: O
OFFSET_BOOK = {
   0:(((0, 0), (-1, 0), (2, 0), (-1, 0), (+2, 0)),
      ((-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)),
      ((-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)),
      ((0, 1), (0, 1), (0, 1), (0, -1), (0, 2))),
   1:(((0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)),
      ((-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)),
      ((-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)),
      ((0, 1), (0, 1), (0, 1), (0, -1), (0, 2))),
   2:(((0, 0)),
      ((0, -1)),
      ((-1, -1)),
      ((-1, 0)))
}

class Piece:
   piece_type = 0
   def __init__(self, piece_type):
      self.piece_type = piece_type
      self.shape = START_PIECES.get(piece_type)
      if piece_type != 0 and piece_type != 3:
         self.offset = 1
      elif piece_type == 0:
         self.offset = 0
      elif piece_type == 3:
         self.offset = 2
   
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
   current_piece = 0

   def __init__(self, current_piece):
      self.game_grid = [['_' for x in range(10)] for y in range(22)]
      self.current_piece = current_piece
      self.piece_x = 0
      self.piece_y = 0
      self.piece_rot = 0

   # 0: left, 1: right, 2: up, 3: down
   def move_piece(self, dir, amt):
      match dir:
         case 0:
            self.piece_x -= amt
         case 1:
            self.piece_x += amt
         case 2:
            self.piece_y -= amt
         case 3:
            self.piece_y += amt
   
   # -1: left, 1: right
   def rotate(self, dir):
      new_rot = (self.piece_rot + dir) % 4
      # Kick translations according to Guideline Tetris SRS
      kick_translations = [(before[0] - after[0], before[1] - after[1]) for before, after in zip(OFFSET_BOOK.get(0)[self.piece_rot], OFFSET_BOOK.get(0)[new_rot])]

      # Test kick translations for collision with filled blocks
      for x_offset, y_offset in kick_translations:
         # Grab area of playing field to check for collision
         area_of_interest = self.game_grid[self.piece_x + x_offset:self.piece_x + len(self.current_piece.shape) + x_offset][self.piece_y + y_offset:self.piece_y + len(self.current_piece.shape) + y_offset]
   
# print(OFFSET_BOOK.get(0)[0])
# print(list(zip(OFFSET_BOOK.get(0)[0], OFFSET_BOOK.get(0)[1])))
# print()
test_grid = [[[x, y] for x in range(10)] for y in range(22)]
for i in test_grid:
   print(i)
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
