from __future__ import division

from const import POINTS
from utils import toStr, getMax, mean, vs

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

      def cannon_move(self, b):
            m = self.blocks_map
            lb = {}
            rb = {}
            ub = {}
            db = {}
            left = range(b['x']-1, -1, -1)
            right = range(b['x'] + 1, 5)
            up = range(b['y'] + 1, 6)
            down = range(b['y']-1, -1, -1)
            for f in left:
                  first = m.get(toStr(f, b['y']), None)
                  if first and first['type'] != 0:
                        for s in range(first['x']-1, -1, -1):
                              second = m.get(toStr(s, b['y']), None)
                              if second and second['type'] != 0:
                                    lb = second
                                    break
                        else:
                              continue
                        break
            for f in right:
                  first = m.get(toStr(f, b['y']), None)
                  if first and first['type'] != 0:
                        for s in range(first['x']+1, 5):
                              second = m.get(toStr(s, b['y']), None)
                              if second and second['type'] != 0:
                                    rb = second
                                    break
                        else:
                              continue
                        break
            for f in up:
                  first = m.get(toStr(b['x'], f), None)
                  if first and first['type'] != 0:
                        for s in range(first['y']+1, 5):
                              second = m.get(toStr(b['x'], s), None)
                              if second and second['type'] != 0:
                                    ub = second
                                    break
                        else:
                              continue
                        break
            for f in down:
                  first = m.get(toStr(b['x'], f), None)
                  if first and first['type'] != 0:
                        for s in range(first['y']-1, -1, -1):
                              second = m.get(toStr(b['x'], s), None)
                              if second and second['type'] != 0:
                                    db = second
                                    break
                        else:
                              continue
                        break

            if lb or rb or ub or db:
                  return {'left': lb, 'right': rb, 'up': ub, 'down': db}
            else:
                  return False

      def get_move_score(self):
            big_score = 0
            big_block = {}
            ai_kill_block = {}
            current_round = self.blocks_map
            move_map = {}
            to_map = {}
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
                  init_score = -9999
                  if right_one and right_one['hasFlip'] and self.side != right_one['side'] and b['type'] != 2 and vs(b, right_one):
                        score = POINTS[right_one['type']]
                        if (right_two and right_two['hasFlip'] and self.side != right_two['side'] and vs(b, right_two)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(b, up_right)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(b, down_right)):
                              if vs(b, right_two):
                                    score = score + POINTS[right_two['type']]/10
                              if vs(b, up_right):
                                    score = score + POINTS[up_right['type']]/10
                              if vs(b, down_right):
                                    score = score + POINTS[down_right['type']]/10
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
                              score = 0 - POINTS[b['type']]
                        if score > init_score:
                              init_score = score
                              move_map[toStr(b['x'], b['y'])] = score
                              to_map[toStr(b['x'], b['y'])] = right_one
                  elif left_one and left_one['hasFlip'] and self.side != left_one['side'] and b['type'] != 2 and vs(b, left_one):
                        score = POINTS[left_one['type']]
                        if (left_two and left_two['hasFlip'] and self.side != left_two['side'] and vs(b, left_two)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(b, up_left)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(b, down_left)):
                              if vs(b, left_two):
                                    score = score + POINTS[left_two['type']]/10
                              if vs(b, up_left):
                                    score = score + POINTS[up_left['type']]/10
                              if vs(b, down_left):
                                    score = score + POINTS[down_left['type']]/10
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
                              score = 0 - POINTS[b['type']]
                        if score > init_score:
                              init_score = score
                              move_map[toStr(b['x'], b['y'])] = score
                              to_map[toStr(b['x'], b['y'])] = left_one
                  elif up_one and up_one['hasFlip'] and self.side != up_one['side'] and b['type'] != 2 and vs(b, up_one):
                        score = POINTS[up_one['type']]
                        if (up_two and up_two['hasFlip'] and self.side != up_two['side'] and vs(b, up_two)) or\
                           (up_left and up_left['hasFlip'] and self.side != up_left['side'] and vs(b, up_left)) or\
                           (up_right and up_right['hasFlip'] and self.side != up_right['side'] and vs(b, up_right)):
                              if vs(b, up_two):
                                    score = score + POINTS[up_two['type']]/10
                              if vs(b, up_left):
                                    score = score + POINTS[up_left['type']]/10
                              if vs(b, up_right):
                                    score = score + POINTS[up_right['type']]/10
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
                              score = 0 - POINTS[b['type']]
                        if score > init_score:
                              init_score = score
                              move_map[toStr(b['x'], b['y'])] = score
                              to_map[toStr(b['x'], b['y'])] = up_one
                  elif down_one and down_one['hasFlip'] and self.side != down_one['side'] and b['type'] != 2 and vs(b, down_one):
                        score = POINTS[down_one['type']]
                        if (down_two and down_two['hasFlip'] and self.side != down_two['side'] and vs(b, down_two)) or\
                           (down_right and down_right['hasFlip'] and self.side != down_right['side'] and vs(b, down_right)) or\
                           (down_left and down_left['hasFlip'] and self.side != down_left['side'] and vs(b, down_left)):
                              if vs(b, down_two):
                                    score = score + POINTS[down_two['type']]/10
                              if vs(b, down_right):
                                    score = score + POINTS[down_right['type']]/10
                              if vs(b, down_left):
                                    score = score + POINTS[down_left['type']]/10
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
                              score = 0 - POINTS[b['type']]
                        if score > init_score:
                              init_score = score
                              move_map[toStr(b['x'], b['y'])] = score
                              to_map[toStr(b['x'], b['y'])] = down_one
                  # can kill, cannon
                  elif b['type'] == 2:
                        if self.cannon_move(b):
                              ck = self.cannon_move(b)
                              for cb in ck:
                                    if ck[cb]:
                                          vb = ck[cb]
                                          cannon_right_one = self.blocks_map.get(toStr(vb['x']+1, vb['y']), None)
                                          cannon_right_two = self.blocks_map.get(toStr(vb['x']+2, vb['y']), None)
                                          cannon_left_one = self.blocks_map.get(toStr(vb['x']-1, vb['y']), None)
                                          cannon_left_two = self.blocks_map.get(toStr(vb['x']-2, vb['y']), None)
                                          cannon_up_one = self.blocks_map.get(toStr(vb['x'], vb['y']+1), None)
                                          cannon_up_two = self.blocks_map.get(toStr(vb['x'], vb['y']+2), None)
                                          cannon_down_one = self.blocks_map.get(toStr(vb['x'], vb['y']-1), None)
                                          cannon_down_two = self.blocks_map.get(toStr(vb['x'], vb['y']-2), None)

                                          if vb['hasFlip'] and self.side != vb['side']:
                                                score = POINTS[vb['type']]
                                                vs1 = 0
                                                vs2 = 0
                                                vs3 = 0
                                                vs4 = 0
                                                if cannon_right_two and cannon_right_two['hasFlip'] and self.side != cannon_right_two['side']:
                                                      vs1 = POINTS[cannon_right_two['type']]/10
                                                if cannon_left_two and cannon_left_two['hasFlip'] and self.side != cannon_left_two['side']:
                                                      vs2 = POINTS[cannon_left_two['type']]/10
                                                if cannon_up_two and cannon_up_two['hasFlip'] and self.side != cannon_up_two['side']:
                                                      vs3 = POINTS[cannon_up_two['type']]/10
                                                if cannon_down_two and cannon_down_two['hasFlip'] and self.side != cannon_down_two['side']:
                                                      vs3 = POINTS[cannon_down_two['type']]/10
                                                if [vs1, vs2, vs3, vs4].count(0) == 3:
                                                      score = score + vs1 + vs2 + vs3 + vs4
                                                if [vs1, vs2, vs3, vs4].count(0) < 3:
                                                      l = [vs1, vs2, vs3, vs4]
                                                      l.remove(0)
                                                      score = score + min(l)

                                                if (cannon_right_one and cannon_right_one['hasFlip'] and self.side != cannon_right_one['side'] and vs(cannon_right_one, b)) or\
                                                   (cannon_left_one and cannon_left_one['hasFlip'] and self.side != cannon_left_one['side'] and vs(cannon_left_one, b)) or\
                                                   (cannon_up_one and cannon_up_one['hasFlip'] and self.side != cannon_up_one['side'] and vs(cannon_up_one, b)) or\
                                                   (cannon_down_one and cannon_down_one['hasFlip'] and self.side != cannon_down_one['side'] and vs(cannon_down_one, b)) or\
                                                   (cannon_right_two and cannon_right_two['hasFlip'] and self.side != cannon_right_two['side'] and cannon_right_two['type'] == 2) or\
                                                   (cannon_left_two and cannon_left_two['hasFlip'] and self.side != cannon_left_two['side'] and cannon_left_two['type'] == 2) or\
                                                   (cannon_up_two and cannon_up_two['hasFlip'] and self.side != cannon_up_two['side'] and cannon_up_two['type'] == 2) or\
                                                   (cannon_down_two and cannon_down_two['hasFlip'] and self.side != cannon_down_two['side'] and cannon_down_two['type'] == 2):
                                                      score = 0 - POINTS[b['type']]
                                                if score > init_score:
                                                      move_map[toStr(b['x'], b['y'])] = score
                                                      to_map[toStr(b['x'], b['y'])] = vb

                                          if not vb['hasFlip']:
                                                score = -(self.expect_score) * 3
                                                if score > init_score:
                                                      move_map[toStr(b['x'], b['y'])] = score
                                                      to_map[toStr(b['x'], b['y'])] = vb
                  else:
                        # TODO
                        continue
                        score = 0
                        move_map[toStr(b['x'], b['y'])] = score
                        to_map[toStr(b['x'], b['y'])] = None

            if move_map:
                  max_block_key = getMax(move_map)
                  big_block = self.blocks_map.get(max_block_key)
                  big_score = max(move_map.values())
                  ai_kill_block = to_map.get(max_block_key)
                  return {'action':'move','score':big_score,'block':ai_kill_block,'from': big_block}
            else:
                  return {'action':'move','score':None,'block':None,'from':None}
            
      
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

            return {'action':'keep','score':big_score,'block':big_block,'from':None}

      def get_flip_score(self):
            cannon_len = sum(b['type'] == 2 for b in self.ai_unflipped)
            big_score = 0
            big_block = {}
            current_round = self.blocks_map
            unflipped = self.ai_unflipped + self.player_unflipped
            unflipped_map = {}
            for b in unflipped:
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
                        init_score = -9999
                        if right_two and right_two['hasFlip'] and self.side != right_two['side'] and right_two['type'] != 0:
                              if right_one and not right_one['hasFlip']:
                                    score = POINTS[right_two['type']] / 50 * cannon_len
                                    if score > init_score:
                                          init_score = score
                                          unflipped_map[toStr(b['x'], b['y'])] = score
                        elif left_two and left_two['hasFlip'] and self.side != left_two['side'] and left_two['type'] != 0:
                              if left_one and not left_one['hasFlip']:
                                    score = POINTS[left_two['type']] / 50 * cannon_len
                                    if score > init_score:
                                          init_score = score
                                          unflipped_map[toStr(b['x'], b['y'])] = score
                        elif up_two and up_two['hasFlip'] and self.side != up_two['side'] and up_two['type'] != 0:
                              if up_one and not up_one['hasFlip']:
                                    score = POINTS[up_two['type']] / 50 * cannon_len
                                    if score > init_score:
                                          init_score = score
                                          unflipped_map[toStr(b['x'], b['y'])] = score
                        elif down_two and down_two['hasFlip'] and self.side != down_two['side'] and down_two['type'] != 0:
                              if down_one and not down_one['hasFlip']:
                                    score = POINTS[down_two['type']] / 50 * cannon_len
                                    if score > init_score:
                                          init_score = score
                                          unflipped_map[toStr(b['x'], b['y'])] = score
                        else:
                              score = self.expect_score / 50
                              unflipped_map[toStr(b['x'], b['y'])] = score
                  # flip, if no cannon in unfliped blocks
                  else:
                        init_score = -9999
                        if right_one and right_one['hasFlip'] and self.side != right_one['side']:
                              score = (self.expect_score - POINTS[right_one['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif left_one and left_one['hasFlip'] and self.side != left_one['side']:
                              score = (self.expect_score - POINTS[left_one['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif up_one and up_one['hasFlip'] and self.side != up_one['side']:
                              score = (self.expect_score - POINTS[up_one['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif down_one and down_one['hasFlip'] and self.side != down_one['side']:
                              score = (self.expect_score - POINTS[down_one['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif up_right and up_right['hasFlip'] and self.side != up_right['side']:
                              score = (self.expect_score - POINTS[up_right['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif up_left and up_left['hasFlip'] and self.side != up_left['side']:
                              score = (self.expect_score - POINTS[up_left['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif down_right and down_right['hasFlip'] and self.side != down_right['side']:
                              score = (self.expect_score - POINTS[down_right['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        elif down_left and down_left['hasFlip'] and self.side != down_left['side']:
                              score = (self.expect_score - POINTS[down_left['type']]) / 50
                              if score > init_score:
                                    init_score = score
                                    unflipped_map[toStr(b['x'], b['y'])] = score
                        else:
                              score = self.expect_score / 50
                              unflipped_map[toStr(b['x'], b['y'])] = score

            if unflipped_map:
                  max_block_key = getMax(unflipped_map)
                  big_block = self.blocks_map.get(max_block_key)
                  big_score = max(unflipped_map.values())
                  return {'action':'flip','score':big_score,'block':big_block,'from':None}
            else:
                  return {'action':'flip','score':None,'big_block':None,'from':None}

