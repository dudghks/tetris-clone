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
   2:(((0, 0), (0, 0)),
       ((0, -1), (0, -1)),
       ((-1, -1), (-1, -1)),
       ((-1, 0), (-1, 0)))
}
print(OFFSET_BOOK[1])
print(OFFSET_BOOK[2])
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
   def check_collision(self, input_grid, input_piece = None):
      if input_piece:
         pass
      else:
         input_piece = self.shape
      for i in range(len(input_grid)):
         for j in range(len(input_grid[i])):
            # if a filled block in the shape array (not '_')
            # is in the same location as one in the input grid
            if input_piece[i][j] != '_' and input_piece[i][j] != '_':
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
   
   def find_area_of_interest(self, x, y, width, height):
      # Grab existing area of playing field
      area = [cols[x:x + width] for cols in self.game_grid[y:y + height]]

      # Find the extent of amount out of bounds
      left = 0 - x
      right = (x + width) - 10
      up = 0 - y
      down = (y + height) - 22

      # Fill in missing values for out of bounds sections
      while left > 0:
         for i in area:
            i.insert(0, 'X')
         left -= 1
      while right > 0:
         for i in area:
            i.append('X')
         right -= 1
      while up > 0:
         area.insert(0, ['X' for i in range(width)])
         up -= 1
      while down > 0:
         area.append(['X' for i in range(width)])
         down -= 1
      
      return area

   # -1: left, 1: right
   def rotate(self, dir):
      new_rot = (self.piece_rot + dir) % 4
      # Kick translations according to Guideline Tetris SRS
      kick_translations = [(before[0] - after[0], before[1] - after[1]) for before, after in zip(OFFSET_BOOK.get(self.current_piece.offset)[self.piece_rot], OFFSET_BOOK.get(0)[new_rot])]
      rotated_piece = self.current_piece.shape
      if dir == -1:
         rotated_piece = self.current_piece.rotate_left()
      elif dir == 1:
         rotated_piece = self.current_piece.rotate_right()
      for i in rotated_piece:
         print(i)
      print('========================================')
      print(kick_translations)
      print('========================================')
      # Test kick translations for collision with filled blocks
      for x_offset, y_offset in kick_translations:
         # Find area of interest for collision checking
         new_spot = self.find_area_of_interest(self.piece_x + x_offset, self.piece_y + y_offset, len(self.current_piece.shape), len(self.current_piece.shape))
         for i in new_spot:
            print(i)
         outcome = self.current_piece.check_collision(new_spot, rotated_piece)
         print(outcome)
         print('==================================')


test_field = Field(Piece(3))
test_field.game_grid = [[[x, y] for x in range(10)] for y in range(22)]
test_field.rotate(1)
print(test_field.current_piece.offset)