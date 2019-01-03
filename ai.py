from __future__ import division

from const import POINTS
from utils import toStr, mean, vs

class Ai(object):

      '''Ai class'''

      def __init__(self, blocks, side):
            self.side = side
            self.blocks = blocks
            self.blocks_map = {}
            self.ai_blocks = []
            self.player_blocks = []
            self.expect_score = 0
            self.ai_flipped = []
            self.ai_unflipped = []
            self.player_flipped = []
            self.player_unflipped = []
            self.make_map()
            self.divide_side()
            self.divide_flip()
            self.expect_flip_score()

      def make_map(self):
            for b in self.blocks:
                  cood = toStr(b['x'], b['y'])
                  if b['piece']:
                        self.blocks_map[cood] = b['piece']
                  else:
                        side = 2 if self.side == 1 else 1
                        empty_piece = {'hasFlip': True, 'type': 0,
                                       'side': side,
                                       'x': b['x'], 'y': b['y']}
                        self.blocks_map[cood] = empty_piece

      def divide_side(self):
            for b in self.blocks:
                  if b['piece']:
                        if b['piece']['side'] == self.side:
                              self.ai_blocks.append(b['piece'])
                        else:
                              self.player_blocks.append(b['piece'])

      def get_block(self, x, y):
            return self.blocks_map.get(toStr(x, y), None)

      def expect_flip_score(self):
            ai_expect = mean([POINTS[block['type']] for block in self.ai_unflipped ])
            player_expect = mean([POINTS[block['type']] for block in self.player_unflipped ])
            self.expect_score = ai_expect - player_expect

      def divide_flip(self):
            for b in self.ai_blocks:
                  if b['hasFlip']:
                        self.ai_flipped.append(b)
                  else:
                        self.ai_unflipped.append(b)
            for b in self.player_blocks:
                  if b['hasFlip']:
                        self.player_flipped.append(b)
                  else:
                        self.player_unflipped.append(b)

      def get_move_score(self):
            big_score = 0
            big_block = {}
            ai_kill_block = {}
            current_round = self.blocks_map
            for b in self.ai_flipped:
                  right_one = self.blocks_map.get(toStr(b['x']+1, b['y']), None)
                  right_two = self.blocks_map.get(toStr(b['x']+2, b['y']), None)
                  right_three = self.blocks_map.get(toStr(b['x']+3, b['y']), None)
                  right_up_two = self.blocks_map.get(toStr(b['x']+1, b['y']+2), None)
                  right_down_two = self.blocks_map.get(toStr(b['x']+1, b['y']-2), None)
                  left_one = self.blocks_map.get(toStr(b['x']-1, b['y']), None)
                  left_two = self.blocks_map.get(toStr(b['x']-2, b['y']), None)
                  left_three = self.blocks_map.get(toStr(b['x']-3, b['y']), None)
                  left_up_two = self.blocks_map.get(toStr(b['x']-1, b['y']+2), None)
                  left_down_two = self.blocks_map.get(toStr(b['x']-1, b['y']-2), None)
                  up_one = self.blocks_map.get(toStr(b['x'], b['y']+1), None)
                  up_two = self.blocks_map.get(toStr(b['x'], b['y']+2), None)
                  up_three = self.blocks_map.get(toStr(b['x'], b['y']+3), None)
                  down_one = self.blocks_map.get(toStr(b['x'], b['y']-1), None)
                  down_two = self.blocks_map.get(toStr(b['x'], b['y']-2), None)
                  down_three = self.blocks_map.get(toStr(b['x'], b['y']-3), None)
                  up_right = self.blocks_map.get(toStr(b['x']+1, b['y']+1), None)
                  up_right_two = self.blocks_map.get(toStr(b['x']+2, b['y']+1), None)
                  up_left = self.blocks_map.get(toStr(b['x']-1, b['y']+1), None)
                  up_left_two = self.blocks_map.get(toStr(b['x']-2, b['y']+1), None)
                  down_right = self.blocks_map.get(toStr(b['x']+1, b['y']-1), None)
                  down_right_two = self.blocks_map.get(toStr(b['x']+2, b['y']-1), None)
                  down_left = self.blocks_map.get(toStr(b['x']-1, b['y']-1), None)
                  down_left_two = self.blocks_map.get(toStr(b['x']-2, b['y']-1), None)
                  
                  # can kill, not cannon
                  if right_one and right_one['hasFlip'] and self.side != right_one['side'] and b['type'] != 2 and vs(b, right_one):
                        score = POINTS[right_one['type']]
                        if (right_two and right_two['hasFlip'] and self.side != right_two['side'] and vs(b, right_two)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(b, up_right)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(b, down_right)):
                              if vs(b, right_two):
                                    socre = score + POINTS[right_two['type']]/10
                              if vs(b, up_right):
                                    socre = score + POINTS[up_right['type']]/10
                              if vs(b, down_right):
                                    socre = score + POINTS[down_right['type']]/10
                              if [vs(b, right_two), vs(b, up_right), vs(b, down_right)].count(True) > 1:
                                    vs1 = POINTS[right_two['type']] if vs(b, right_two) else 0
                                    vs2 = POINTS[up_right['type']] if vs(b, up_right) else 0
                                    vs3 = POINTS[down_right['type']] if vs(b, down_right) else 0
                                    score = score + min([vs1, vs2, vs3])
                        # kill and then be killed, killed by cannon or others
                        if (right_two and right_two['hasFlip'] and self.side != right_two['side'] and vs(right_two, b)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(up_right, b)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(down_right, b)) or\
                           (right_three and right_three['hasFlip'] and self.side != right_three['side'] and right_three['type'] == 2) or\
                           (right_up_two and right_up_two['hasFlip'] and self.side != right_up_two['side'] and right_up_two['type'] == 2) or\
                           (right_down_two and right_down_two['hasFlip'] and self.side != right_down_two['side'] and right_down_two['type'] == 2):
                              score = score - POINTS[b['type']]
                        if score > big_score:
                              big_score = score
                              big_block = right_one
                              ai_kill_block = b
                  if left_one and left_one['hasFlip'] and self.side != left_one['side'] and b['type'] != 2 and vs(b, left_one):
                        score = POINTS[left_one['type']]
                        if (left_two and left_two['hasFlip'] and self.side != left_two['side'] and vs(b, left_two)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(b, up_left)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(b, down_left)):
                              if vs(b, left_two):
                                    socre = score + POINTS[left_two['type']]/10
                              if vs(b, up_left):
                                    socre = score + POINTS[up_left['type']]/10
                              if vs(b, down_left):
                                    socre = score + POINTS[down_left['type']]/10
                              if [vs(b, left_two), vs(b, up_left), vs(b, down_left)].count(True) > 1:
                                    vs1 = POINTS[left_two['type']] if vs(b, left_two) else 0
                                    vs2 = POINTS[up_left['type']] if vs(b, up_left) else 0
                                    vs3 = POINTS[down_left['type']] if vs(b, down_left) else 0
                                    score = score + min([vs1, vs2, vs3])
                        if (left_two and left_two['hasFlip'] and self.side != left_two['side'] and vs(left_two, b)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(up_left, b)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(down_left, b)) or\
                           (left_three and left_three['hasFlip'] and self.side != left_three['side'] and left_three['type'] == 2) or\
                           (left_up_two and left_up_two['hasFlip'] and self.side != left_up_two['side'] and left_up_two['type'] == 2) or\
                           (left_down_two and left_down_two['hasFlip'] and self.side != left_down_two['side'] and left_down_two['type'] == 2):
                              score = score - POINTS[b['type']]
                        if score > big_score:
                              big_score = score
                              big_block = left_one
                              ai_kill_block = b
                  if up_one and up_one['hasFlip'] and self.side != up_one['side'] and b['type'] != 2 and vs(b, up_one):
                        score = POINTS[up_one['type']]
                        if (up_two and up_two['hasFlip'] and self.side != up_two['side'] and vs(b, up_two)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(b, up_left)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(b, up_right)):
                              if vs(b, up_two):
                                    socre = score + POINTS[up_two['type']]/10
                              if vs(b, up_left):
                                    socre = score + POINTS[up_left['type']]/10
                              if vs(b, up_right):
                                    socre = score + POINTS[up_right['type']]/10
                              if [vs(b, up_two), vs(b, up_left), vs(b, up_right)].count(True) > 1:
                                    vs1 = POINTS[up_two['type']] if vs(b, up_two) else 0
                                    vs2 = POINTS[up_left['type']] if vs(b, up_left) else 0
                                    vs3 = POINTS[up_right['type']] if vs(b, up_right) else 0
                                    score = score + min([vs1, vs2, vs3])
                        if (up_two and up_two['hasFlip'] and self.side != up_two['side'] and vs(up_two, b)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(up_left, b)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(up_right, b)) or\
                           (up_three and up_three['hasFlip'] and self.side != up_three['side'] and up_three['type'] == 2) or\
                           (up_right_two and up_right_two['hasFlip'] and self.side != up_right_two['side'] and up_right_two['type'] == 2) or\
                           (up_left_two and up_left_two['hasFlip'] and self.side != up_left_two['side'] and up_left_two['type'] == 2):
                              score = score - POINTS[b['type']]
                        if score > big_score:
                              big_score = score
                              big_block = up_one
                              ai_kill_block = b
                  if down_one and down_one['hasFlip'] and self.side != down_one['side'] and b['type'] != 2 and vs(b, down_one):
                        score = POINTS[down_one['type']]
                        if (down_two and down_two['hasFlip'] and self.side != down_two['side'] and vs(b, down_two)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(b, down_right)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(b, down_left)):
                              if vs(b, down_two):
                                    socre = score + POINTS[down_two['type']]/10
                              if vs(b, down_right):
                                    socre = score + POINTS[down_right['type']]/10
                              if vs(b, down_left):
                                    socre = score + POINTS[down_left['type']]/10
                              if [vs(b, down_two), vs(b, down_right), vs(b, down_left)].count(True) > 1:
                                    vs1 = POINTS[down_two['type']] if vs(b, down_two) else 0
                                    vs2 = POINTS[down_right['type']] if vs(b, down_right) else 0
                                    vs3 = POINTS[down_left['type']] if vs(b, down_left) else 0
                                    score = score + min([vs1, vs2, vs3])
                        if (down_two and down_two['hasFlip'] and self.side != down_two['side'] and vs(down_two, b)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(down_right, b)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(down_left, b)) or\
                           (down_three and down_three['hasFlip'] and self.side != down_three['side'] and down_three['type'] == 2) or\
                           (down_right_two and down_right_two['hasFlip'] and self.side != down_right_two['side'] and down_right_two['type'] == 2) or\
                           (down_left_two and down_left_two['hasFlip'] and self.side != down_left_two['side'] and down_left_two['type'] == 2):
                              score = score - POINTS[b['type']]
                        if score > big_score:
                              big_score = score
                              big_block = down_one
                              ai_kill_block = b
                  # can kill, cannon
                  if right_two and right_two['hasFlip'] and self.side != right_two['side'] and b['type'] == 2:
                        score = POINTS[right_two['type']]
                        if score > big_score:
                              big_score = score
                              big_block = right_two
                              ai_kill_block = b
                  if left_two and left_two['hasFlip'] and self.side != left_two['side'] and b['type'] == 2:
                        score = POINTS[left_two['type']]
                        if score > big_score:
                              big_score = score
                              big_block = left_two
                              ai_kill_block = b
                  if up_two and up_two['hasFlip'] and self.side != up_two['side'] and b['type'] == 2:
                        score = POINTS[up_two['type']]
                        if score > big_score:
                              big_score = score
                              big_block = up_two
                              ai_kill_block = b
                  if down_two and down_two['hasFlip'] and self.side != down_two['side'] and b['type'] == 2:
                        score = POINTS[down_two['type']]
                        if score > big_score:
                              big_score = score
                              big_block = down_two
                              ai_kill_block = b
                  # can kill, cannon steal
                  if right_two and not right_two['hasFlip'] and b['type'] == 2:
                        score = -(self.expect_score) * 3
                        if score > big_score:
                              big_score = score
                              big_block = right_two
                              ai_kill_block = b
                  if left_two and not left_two['hasFlip'] and b['type'] == 2:
                        score = -(self.expect_score) * 3
                        if score > big_score:
                              big_score = score
                              big_block = left_two
                              ai_kill_block = b
                  if up_two and not up_two['hasFlip'] and b['type'] == 2:
                        score = -(self.expect_score) * 3
                        if score > big_score:
                              big_score = score
                              big_block = up_two
                              ai_kill_block = b
                  if down_two and not down_two['hasFlip'] and b['type'] == 2:
                        score = -(self.expect_score) * 3
                        if score > big_score:
                              big_score = score
                              big_block = down_two
                              ai_kill_block = b
                  # move, will be killed
                              
            return {'action': 'move', 'score': big_score, 'block': big_block, 'from': ai_kill_block}
      
      def get_keep_score(self):
            big_score = 0
            big_block = {}
            current_round = self.blocks_map
            for b in self.ai_flipped:
                  right_one = self.blocks_map.get(toStr(b['x']+1, b['y']), None)
                  right_two = self.blocks_map.get(toStr(b['x']+2, b['y']), None)
                  left_one = self.blocks_map.get(toStr(b['x']-1, b['y']), None)
                  left_two = self.blocks_map.get(toStr(b['x']-2, b['y']), None)
                  up_one = self.blocks_map.get(toStr(b['x'], b['y']+1), None)
                  up_two = self.blocks_map.get(toStr(b['x'], b['y']+2), None)
                  down_one = self.blocks_map.get(toStr(b['x'], b['y']-1), None)
                  down_two = self.blocks_map.get(toStr(b['x'], b['y']-2), None)
                  up_right = self.blocks_map.get(toStr(b['x']+1, b['y']+1), None)
                  up_left = self.blocks_map.get(toStr(b['x']-1, b['y']+1), None)
                  down_right = self.blocks_map.get(toStr(b['x']+1, b['y']-1), None)
                  down_left = self.blocks_map.get(toStr(b['x']-1, b['y']-1), None)

                  # keep, protect ai
                  if right_one and right_one['hasFlip'] and self.side == right_one['side']:
                        if right_two and right_two['hasFlip'] and self.side != right_two['side'] or\
                           up_right and up_right['hasFlip'] and self.side != up_right['side'] or\
                           down_right and down_right['hasFlip'] and self.side != down_right['side']:
                              if vs(right_two, right_one) or vs(up_right, right_one) or vs(down_right, right_one):
                                    score = 0
                                    if vs(b, right_two):
                                          score = POINTS[right_two['type']] - POINTS[right_one['type']]
                                    if vs(b, up_right):
                                          score = POINTS[up_right['type']] - POINTS[right_one['type']]
                                    if vs(b, down_right):
                                          score = POINTS[down_right['type']] - POINTS[right_one['type']]
                                    if [vs(b, right_two), vs(b, up_right), vs(b, down_right)].count(True) > 1:
                                          vs1 = POINTS[right_two['type']] if vs(b, right_two) else 0
                                          vs2 = POINTS[up_right['type']] if vs(b, up_right) else 0
                                          vs3 = POINTS[down_right['type']] if vs(b, down_right) else 0
                                          score = score + min([vs1, vs2, vs3])
                                    if score > big_score:
                                          big_score = score
                                          big_block = b
                  if left_one and left_one['hasFlip'] and self.side == left_one['side']:
                        if left_two and left_two['hasFlip'] and self.side != left_two['side'] or\
                           up_left and up_left['hasFlip'] and self.side != up_left['side'] or\
                           down_left and down_left['hasFlip'] and self.side != down_left['side']:
                              if vs(left_two, left_one) or vs(up_left, left_one) or vs(down_left, left_one):
                                    score = 0
                                    if vs(b, left_two):
                                          score = POINTS[left_two['type']] - POINTS[left_one['type']]
                                    if vs(b, up_left):
                                          score = POINTS[up_left['type']] - POINTS[left_one['type']]
                                    if vs(b, down_left):
                                          score = POINTS[down_left['type']] - POINTS[left_one['type']]
                                    if [vs(b, left_two), vs(b, up_left), vs(b, down_left)].count(True) > 1:
                                          vs1 = POINTS[left_two['type']] if vs(b, right_two) else 0
                                          vs2 = POINTS[up_left['type']] if vs(b, up_left) else 0
                                          vs3 = POINTS[down_left['type']] if vs(b, down_left) else 0
                                          score = score + min([vs1, vs2, vs3])
                                    if score > big_score:
                                          big_score = score
                                          big_block = b
                  if up_one and up_one['hasFlip'] and self.side == up_one['side']:
                        if up_two and up_two['hasFlip'] and self.side != up_two['side'] or\
                           up_right and up_right['hasFlip'] and self.side != up_right['side'] or\
                           up_left and up_left['hasFlip'] and self.side != up_left['side']:
                              if vs(up_two, up_one) or vs(up_right, up_one) or vs(up_left, up_one):
                                    score = 0
                                    if vs(b, up_two):
                                          score = POINTS[up_two['type']] - POINTS[up_one['type']]
                                    if vs(b, up_right):
                                          score = POINTS[up_right['type']] - POINTS[up_one['type']]
                                    if vs(b, up_left):
                                          score = POINTS[up_left['type']] - POINTS[up_one['type']]
                                    if [vs(b, up_two), vs(b, up_right), vs(b, up_left)].count(True) > 1:
                                          vs1 = POINTS[up_two['type']] if vs(b, up_two) else 0
                                          vs2 = POINTS[up_right['type']] if vs(b, up_right) else 0
                                          vs3 = POINTS[up_left['type']] if vs(b, up_left) else 0
                                          score = score + min([vs1, vs2, vs3])
                                    if score > big_score:
                                          big_score = score
                                          big_block = b
                  if down_one and down_one['hasFlip'] and self.side == down_one['side']:
                        if down_two and down_two['hasFlip'] and self.side != down_two['side'] or\
                           down_right and down_right['hasFlip'] and self.side != down_right['side'] or\
                           down_left and down_left['hasFlip'] and self.side != down_left['side']:
                              if vs(down_two, down_one) or vs(down_right, down_one) or vs(down_left, down_one):
                                    score = 0
                                    if vs(b, down_two):
                                          score = POINTS[down_two['type']] - POINTS[down_one['type']]
                                    if vs(b, down_right):
                                          score = POINTS[down_right['type']] - POINTS[down_one['type']]
                                    if vs(b, down_left):
                                          score = POINTS[down_left['type']] - POINTS[down_one['type']]
                                    if [vs(b, down_two), vs(b, down_right), vs(b, down_left)].count(True) > 1:
                                          vs1 = POINTS[down_two['type']] if vs(b, down_two) else 0
                                          vs2 = POINTS[down_right['type']] if vs(b, down_right) else 0
                                          vs3 = POINTS[down_left['type']] if vs(b, down_left) else 0
                                          score = score + min([vs1, vs2, vs3])
                                    if score > big_score:
                                          big_score = score
                                          big_block = b

                  # keep, will be killed
                  if (right_one and self.side != right_one['side'] and vs(right_one, b)) \
                     or (left_one and self.side != left_one['side'] and vs(left_one, b)) \
                     or (up_one and self.side != up_one['side'] and vs(up_one, b)) \
                     or (down_one and self.side != down_one['side'] and vs(down_one, b)) \
                     or (right_two and self.side != right_two['side'] and right_two['type'] == 2) \
                     or (left_two and self.side != left_two['side'] and left_two['type'] == 2) \
                     or (up_two and self.side != up_two['side'] and up_two['type'] == 2) \
                     or (down_two and self.side != down_two['side'] and down_two['type'] == 2):
                        score = -POINTS[b['type']]
                        if score > big_score:
                              big_score = score
                              big_block = b

            return {'action': 'keep', 'score': big_score, 'block': big_block, 'from': None}

      def get_flip_score(self):
            cannon_len = sum(b['type'] == 2 for b in self.ai_unflipped)
            big_score = 0
            big_block = {}
            current_round = self.blocks_map
            for b in self.player_flipped:
                  right_one = self.blocks_map.get(toStr(b['x']+1, b['y']), None)
                  right_two = self.blocks_map.get(toStr(b['x']+2, b['y']), None)
                  left_one = self.blocks_map.get(toStr(b['x']-1, b['y']), None)
                  left_two = self.blocks_map.get(toStr(b['x']-2, b['y']), None)
                  up_one = self.blocks_map.get(toStr(b['x'], b['y']+1), None)
                  up_two = self.blocks_map.get(toStr(b['x'], b['y']+2), None)
                  down_one = self.blocks_map.get(toStr(b['x'], b['y']-1), None)
                  down_two = self.blocks_map.get(toStr(b['x'], b['y']-2), None)
                  up_right = self.blocks_map.get(toStr(b['x']+1, b['y']+1), None)
                  up_left = self.blocks_map.get(toStr(b['x']-1, b['y']+1), None)
                  down_right = self.blocks_map.get(toStr(b['x']+1, b['y']-1), None)
                  down_left = self.blocks_map.get(toStr(b['x']-1, b['y']-1), None)

                  # flip, if cannons in unfliped blocks
                  if cannon_len > 0:
                        if right_one and not right_one['hasFlip'] and right_two and not right_two['hasFlip']:
                              score = POINTS[b['type']] / 50 * cannon_len
                              if score > big_score:
                                    big_score = score
                                    big_block = right_two
                              current_round.pop(toStr(right_two['x'], right_two['y']), None)
                        if left_one and not left_one['hasFlip'] and left_two and not left_two['hasFlip']:
                              score = POINTS[b['type']] / 50 * cannon_len
                              if score > big_score:
                                    big_score = score
                                    big_block = left_two
                              current_round.pop(toStr(left_two['x'], left_two['y']), None)
                        if up_one and not up_one['hasFlip'] and up_two and not up_two['hasFlip']:
                              score = POINTS[b['type']] / 50 * cannon_len
                              if score > big_score:
                                    big_score = score
                                    big_block = up_two
                              current_round.pop(toStr(up_two['x'], up_two['y']), None)
                        if down_one and not down_one['hasFlip'] and down_two and not down_two['hasFlip']:
                              score = POINTS[b['type']] / 50 * cannon_len
                              if score > big_score:
                                    big_score = score
                                    big_block = down_two
                              current_round.pop(toStr(down_two['x'], down_two['y']), None)
                  # flip, if no cannon in unfliped blocks
                  else:
                        if right_one and not right_one['hasFlip']:
                              score = (self.expect_score - POINTS[b['type']]) / 50
                              if score > big_score:
                                    big_score = score
                                    big_block = right_one
                              current_round.pop(toStr(right_one['x'], right_one['y']), None)
                        if left_one and not left_one['hasFlip']:
                              score = (self.expect_score - POINTS[b['type']]) / 50
                              if score > big_score:
                                    big_score = score
                                    big_block = left_one
                              current_round.pop(toStr(left_one['x'], left_one['y']), None)
                        if up_one and not up_one['hasFlip']:
                              score = (self.expect_score - POINTS[b['type']]) / 50
                              if score > big_score:
                                    big_score = score
                                    big_block = up_one
                              current_round.pop(toStr(up_one['x'], up_one['y']), None)
                        if down_one and not down_one['hasFlip']:
                              score = (self.expect_score - POINTS[b['type']]) / 50
                              if score > big_score:
                                    big_score = score
                                    big_block = down_one
                              current_round.pop(toStr(down_one['x'], down_one['y']), None)

            other_score = self.expect_score / 50
            if other_score > big_score:
                  big_score = other_score
                  current_unflipped = {}
                  for k, v in current_round.iteritems():
                        if v and not v['hasFlip']:
                              current_unflipped[k] = current_round[k]
                  if current_unflipped:
                        big_block = current_unflipped.values()[0]

            return {'action': 'flip', 'score': big_score, 'block': big_block, 'from': None}
                  
