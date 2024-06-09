from flask import Flask, render_template, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/api/click", methods=['POST'])
def click():
    name = request.json.get('name', None)
    if not name:
        return jsonify({'error': 'Invalid request'}), 400
    if r.sismember('banned_users', name):
        return jsonify({'error': 'User is banned'}), 403
    r.zincrby('leaderboard', 1, f'clicks:{name}')
    return jsonify({'message': 'Click registered!'})

@app.route("/api/leaderboard")
def get_leaderboard():
    leaderboard = r.zrevrange('leaderboard', 0, 9, withscores=True)
    return jsonify(leaderboard)

@app.route("/api/reset", methods=['POST'])
def reset():
    r.flushall()
    return "Leaderboard reset!"

@app.route("/api/remove", methods=['POST'])
def remove():
    name = request.json.get('name', None)
    if not name:
        return jsonify({'error': 'Invalid request'}), 400
    r.zrem('leaderboard', f'clicks:{name}')
    r.sadd('banned_users', name)
    return "User removed and banned from leaderboard!"

@app.route("/api/check_ban", methods=['POST'])
def check_ban():
    name = request.json.get('name', None)
    if not name:
        return jsonify({'error': 'Invalid request'}), 400
    if r.sismember('banned_users', name):
        return jsonify({'banned': True}), 403
    return jsonify({'banned': False})

if __name__ == "__main__":
    app.run(debug=True)
