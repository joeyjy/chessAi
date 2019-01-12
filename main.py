import logging

from flask import Flask, jsonify, request

from ai import Ai

LOG_FORMAT = "%(message)s"
logging.basicConfig(filename='/tmp/ai.log', level=logging.ERROR, format=LOG_FORMAT)

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/', methods=['POST'])
def index():
    rawData = request.get_json()
    if rawData:
        fetch = [ block for block in rawData['boardInfo']['blocks'] ]
        blocks = sorted(fetch, key=lambda k: k['x'])

        ai = Ai(blocks, rawData['side'])

        #logging.debug('EXPECT:' + str(ai.expect_score))
        move = ai.get_move_score()
        #logging.debug('MOVE:' + str(move))
        keep = ai.get_keep_score()
        #logging.debug('KEEP:' + str(keep))
        flip = ai.get_flip_score()
        #logging.debug('FLIP:' + str(flip))
        collector = {'move': move, 'keep': keep, 'flip': flip}

        scores = {'move': move['score'], 'keep': keep['score'], 'flip': flip['score']}
        action = max(scores, key=scores.get)
        if action == 'keep':
            scores.pop('keep')
            action = max(scores, key=scores.get)
        result = collector[action]
        logging.error(str({'EXPECT': ai.expect_score, 'MOVE': move, 'KEEP': keep, 'FLIP':flip, 'RESULT': result, 'DETAIL': {'move': move['detail'], 'keep': keep['detail'], 'flip': flip['detail']}}))

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
            # TODO
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
