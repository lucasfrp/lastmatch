from flask import Flask, jsonify, request
from lib.handler import PlayerHandler
app = Flask(__name__)


@app.route('/get/player/lastmatch/<summoner>')
def last_match(summoner):
    win = request.args.get('win', None)
    p = PlayerHandler(summoner)
    m = p.get_last_match(win)
    return jsonify(m.get_player_status(p.account_id))


app.run(host='0.0.0.0', port=80)