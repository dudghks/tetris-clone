import pygame
import random

screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()

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

COLORS = {
   'I':(0, 255, 255),
   'J':(0, 0, 255),
   'L':(255, 102, 0),
   'O':(255, 255, 0),
   'S':(0, 255, 0),
   'T':(106, 13, 173),
   'Z':(255, 0, 0),
   '_':(100, 100, 100)
}

# 0: I | 1: J, L, S, T, Z | 2: O
OFFSET_BOOK = {
   0:(((0, 0), (1, 0), (-2, 0), (1, 0), (-2, 0)),
      ((1, 0), (0, 0), (0, 0), (0, 1), (0, -2)),
      ((1, 1), (-1, 1), (2, 1), (-1, 0), (2, 0)),
      ((0, 1), (0, 1), (0, 1), (0, -1), (0, 2))),
   1:(((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
      ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
      ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
      ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2))),
   2:(((0, 0),),
      ((0, -1),),
      ((1, -1),),
      ((1, 0),))
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
   def check_collision(self, input_grid, input_piece = None):
      if input_piece:
         pass
      else:
         input_piece = self.shape
      for i in range(len(input_grid)):
         for j in range(len(input_grid[i])):
            # if both test blocks are filled, there is a collision
            if input_piece[i][j] != '_' and input_grid[i][j] != '_':
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
      self.current_piece = Piece(current_piece)
      if current_piece == 0:
         self.piece_x = 2
         self.piece_y = 0
      else:
         self.piece_x = 3
         self.piece_y = 2
      self.piece_rot = 0
      self.held_piece_id = None
      self.time_on_ground = 0
      self.lock_down_stall = 15
      self.gravity = 1
      self.counter = 0
      self.queue = []
   
   def find_area_of_interest(self, x, y, width, height):
      # Grab existing area of playing field
      area = [cols[(0 if x < 0 else x):x + width] for cols in self.game_grid[(0 if y < 0 else y):y + height]]
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
      kick_translations = [(after[0] - before[0], after[1] - before[1]) for before, after in zip(OFFSET_BOOK.get(self.current_piece.offset)[self.piece_rot], OFFSET_BOOK.get(self.current_piece.offset)[new_rot])]
      rotated_piece = self.current_piece.shape
      if dir == -1:
         rotated_piece = self.current_piece.rotate_left()
      elif dir == 1:
         rotated_piece = self.current_piece.rotate_right()
      
      # Test kick translations for collision with filled blocks
      for offsets in kick_translations:
         x_offset, y_offset = offsets
         # Find area of interest for collision checking
         new_spot = self.find_area_of_interest(self.piece_x + x_offset, self.piece_y + y_offset, len(self.current_piece.shape), len(self.current_piece.shape))
         outcome = self.current_piece.check_collision(new_spot, rotated_piece)
         if not outcome:
            self.piece_x += x_offset
            self.piece_y  += y_offset
            self.piece_rot = new_rot
            self.current_piece.shape = rotated_piece
            break
      
      if not self.piece_is_floating():
         self.lock_down_stall -= 1
   
   def move(self, dir_x, dir_y):
      new_spot = self.find_area_of_interest(self.piece_x + dir_x, self.piece_y + dir_y, len(self.current_piece.shape), len(self.current_piece.shape))
      collision = self.current_piece.check_collision(new_spot)
      if not collision:
         self.piece_x += dir_x
         self.piece_y += dir_y
      
      if not self.piece_is_floating():
         self.lock_down_stall -= 1
      return collision

   def generate_queue(self):
      options = [0, 1, 2, 3, 4, 5, 6]
      output = []
      while len(options) > 0:
         picked = random.randint(0, len(options) - 1)
         output.append(options[picked])
         del options[picked]
      self.queue += (output)

   def generate_new_piece(self, from_hold):
      if from_hold and self.held_piece_id:
         new_piece = self.held_piece_id
      else:
         new_piece = self.queue[0]
         del self.queue[0]
      self.current_piece = Piece(new_piece)
      if new_piece == 0:
         self.piece_x = 2
         self.piece_y = 0
      else:
         self.piece_x = 3
         self.piece_y = 2
      self.piece_rot = 0
      self.held_piece_id = None
      self.time_on_ground = 0
      self.lock_down_stall = 15
      new_spot = self.find_area_of_interest(self.piece_x, self.piece_y, len(self.current_piece.shape), len(self.current_piece.shape))
      piece_invalid = self.current_piece.check_collision(new_spot)
      if len(self.queue) < 7:
         self.generate_queue()
      
      if piece_invalid:
         return False

   def place_piece(self):
      for y, i in enumerate(self.current_piece.shape):
         for x, j in enumerate(i):
            if 0 <= self.piece_x + x <= len(self.game_grid[0]) and 0 <= self.piece_y + y <= len(self.game_grid) and j != '_':
               self.game_grid[self.piece_y + y][self.piece_x + x] = j

   def piece_is_floating(self):
      # If the piece undergoes a collision if it is one block lower, then it is not floating
      surface_check = self.find_area_of_interest(self.piece_x, self.piece_y + 1, len(self.current_piece.shape), len(self.current_piece.shape))
      return not self.current_piece.check_collision(surface_check)

   def hard_drop(self):
      while self.piece_is_floating():
         self.piece_y += 1
      else:
         self.place_piece()
         self.generate_new_piece(False)
         self.clear_filled_rows()

   def update_piece_status(self):
      if self.time_on_ground >= 30:
         self.place_piece()
         self.generate_new_piece(False)
         self.clear_filled_rows()
         return 0

      if self.piece_is_floating():
         self.time_on_ground = 0
      else:
         self.time_on_ground += 1

   def find_filled_rows(self):
      counter = []
      for idx, i in enumerate(self.game_grid):
         if not '_' in i:
            counter.append(idx)
      return counter

   def update_gravity(self, magnitude = 1):
      speed = (0.8-((self.gravity)*0.007))**(self.gravity-1)
      if self.piece_is_floating():
         self.counter += 1/60 * magnitude
      else:
         self.counter = 0

      while self.counter > speed and self.piece_is_floating():
         self.piece_y += 1
         self.counter -= speed
      
   def clear_filled_rows(self):
      rows_to_del = self.find_filled_rows()
      for i in rows_to_del:
         del self.game_grid[i]
         self.game_grid.insert(0, ['_' for x in range(10)])
      return len(rows_to_del)

   def hold(self):
      temp = self.current_piece.piece_type
      if self.held_piece_id:
         self.generate_new_piece(True)
         self.held_piece_id = temp
      else:
         self.generate_new_piece(True)
         self.held_piece_id = temp

   def display(self, x_offset, y_offset):
      for y, i in enumerate(self.game_grid):
         for x, j in enumerate(i):
            # pass
            pygame.draw.rect(screen, COLORS.get(j), (x * 25 + x_offset, y * 25 + y_offset, 25, 25))
      for y, i in enumerate(self.current_piece.shape):
         for x, j in enumerate(i):
            if j != '_':
               pygame.draw.rect(screen, COLORS.get(j), ((x + self.piece_x) * 25 + x_offset, (y + self.piece_y) * 25 + y_offset, 25, 25))
      pygame.draw.rect(screen, (150, 150, 150), (260 + x_offset, 0 + y_offset, 125, 395))
      for k in range(5):
         queue_piece = START_PIECES.get(self.queue[k])
         for y, i in enumerate(queue_piece):
            for x, j in enumerate(i):
               if j != '_':
                  if self.queue[k] == 0:
                     pygame.draw.rect(screen, COLORS.get(j), (x * 25 + x_offset + 250, (y + 3*k) * 25 + y_offset, 25, 25))
                  else:
                     pygame.draw.rect(screen, COLORS.get(j), (x * 25 + x_offset + 275, (y + 3*k) * 25 + y_offset + 25, 25, 25))


            

   

# Main Loop
running = True
background = pygame.transform.scale(pygame.image.load('background.jpg'), (1600, 900))
soft_drop = False
move_left = False
move_right = False
das_counter = 0
test_field = Field(2)
test_field.generate_queue()
test_field.game_grid = [
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
['T', '_', '_', 'T', '_', '_', '_', '_', '_', '_'],
['T', '_', '_', 'T', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', 'T', '_', '_', '_', '_', '_', '_'],
['_', 'T', 'T', 'T', '_', '_', '_', '_', '_', '_']]

while running:
   # Background
   screen.fill((0, 0, 0))
   screen.blit(background, (0, 0))
   clock.tick(60)
   # Handle key inputs from the player
   keys = pygame.key.get_pressed()
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

      # if keystroke is pressed check for controls
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_RIGHT:
            test_field.move(1, 0)
            move_right = True
         if event.key == pygame.K_LEFT:
            test_field.move(-1, 0)
            move_left = True
         if event.key == pygame.K_DOWN:
            soft_drop = True
         if event.key == pygame.K_UP:
            test_field.hard_drop()
         if event.key == pygame.K_z:
            test_field.rotate(-1)
         if event.key == pygame.K_x:
            test_field.rotate(1)
         if event.key == pygame.K_c:
            test_field.hold()
         if event.key == pygame.K_e:
            test_field.gravity += 1
         if event.key == pygame.K_q:
            test_field.gravity -= 1
      
      if event.type == pygame.KEYUP:
         if event.key == pygame.K_RIGHT:
            move_right = False
            if not move_left:
               das_counter = 0
         if event.key == pygame.K_LEFT:
            move_left = False
            if not move_right:
               das_counter = 0
         if event.key == pygame.K_DOWN:
            soft_drop = False

   if move_left or move_right:
      das_counter += 1

   if das_counter > 8 and das_counter % 2 == 1:
      if move_left:
         test_field.move(-1, 0)
      if move_right:
         test_field.move(1, 0)

   test_field.update_piece_status()
   if soft_drop:
      test_field.update_gravity(20)
   test_field.update_gravity()
   test_field.display(558, 134)

   
   pygame.display.update()
