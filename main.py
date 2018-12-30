from flask import Flask, jsonify, request

from ai import Ai

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/', methods=['POST'])
def index():
    rawData = request.get_json()
    if rawData:
        fetch = [ block for block in rawData['boardInfo']['blocks'] ]
        blocks = sorted(fetch, key=lambda k: k['x'])

        ai = Ai(blocks, rawData['side'])

        print 'EXPECT: '
        print ai.expect_score
        print '--------------------'
        print 'MOVE: '
        move = ai.get_move_score()
        print move
        print 'KEEP: '
        keep = ai.get_keep_score()
        print keep
        print 'FLIP: '
        flip = ai.get_flip_score()
        print flip
        collector = {'move': move, 'keep': keep, 'filp': flip}

        scores = {'move': move['score'], 'keep': keep['score'], 'filp': flip['score']}
        action = max(scores, key=scores.get)
        result = collector[action]
        print 'RESULT: '
        print result
        if move['score'] == 0 and keep['score'] == 0 and flip['score'] == 0:
            if flip['block']:
                return jsonify(
                    {
                        'pid': flip['block']['id'],
                        'type': 'flip',
                        'x': None,
                        'y': None
                    }
                )
            else:
                return jsonify(
                    {
                        'pid': None,
                        'type': 'keep',
                        'x': None,
                        'y': None
                    }
                )

        if result['action'] == 'move':
            return jsonify(
                {
                    'pid': result['from']['id'],
                    'type': 'move',
                    'x': result['block']['x'],
                    'y': result['block']['y']
                }
            )
        elif result['action'] == 'flip':
            return jsonify(
                {
                    'pid': result['block']['id'],
                    'type': 'flip',
                    'x': None,
                    'y': None
                }
            )
        else:
            return jsonify(
                {
                    'pid': None,
                    'type': 'keep',
                    'x': None,
                    'y': None
                }
            )
        return jsonify(
            {
                'pid': None,
                'type': 'keep',
                'x': None,
                'y': None
            }
        )

if __name__ == '__main__':
    app.run()
