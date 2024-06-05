from flask import Flask, render_template, request
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
    print(request.json)
    name = request.json.get('name', None)
    if not name:
        return "Invalid request", 400
    r.zincrby('leaderboard', 1, f'clicks:{name}')
    return "Click registered!"

@app.route("/api/leaderboard")
def get_leaderboard():
    leaderboard = r.zrevrange('leaderboard', 0, 9, withscores=True)
    # convert to json
    return list(leaderboard)

@app.route("/api/reset", methods=['POST'])
def reset():
    r.flushall()
    return "Leaderboard reset!"