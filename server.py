from flask import Flask, request, jsonify, send_from_directory
from threading import Thread
import json, subprocess, os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'id_login.html')

@app.route('/check-id', methods=['POST'])
def check_id():
    data = request.get_json()
    with open('id.json') as f:
        real_id = json.load(f).get('access_id')
    return "ok" if data.get('id') == real_id else "no"

@app.route('/connect')
def connect():
    return send_from_directory('static', 'connect.html')

@app.route('/start-bot', methods=['POST'])
def start_bot():
    data = request.get_json()
    host = data['host']
    port = data['port']
    version = data['version']
    def run_bot():
        subprocess.run(["node", "bot.js", host, port, version])
    Thread(target=run_bot).start()
    return "Bot başlatılıyor..."

@app.route('/panel')
def panel():
    return send_from_directory('static', 'panel.html')

@app.route('/players')
def players():
    with open("players.json") as f:
        return jsonify({"players": json.load(f)})

@app.route('/disconnect')
def disconnect():
    os.system("pkill -f bot.js")
    return "Bot çıkarıldı."

@app.route('/versions')
def versions():
    edition = request.args.get('type', 'java')
    if edition == 'bedrock':
        return jsonify({"versions": [
            "1.20.40", "1.20.30", "1.19.83", "1.19.63",
            "1.18.12", "1.17.41", "1.16.221", "1.14.60"
        ]})
    else:
        return jsonify({"versions": [
            "1.21.5", "1.21.4", "1.21.3", "1.21.2", "1.21.1",
            "1.20.4", "1.20.1", "1.20", "1.19.4", "1.19.2",
            "1.18.2", "1.17.1", "1.16.5", "1.15.2", "1.12.2", "1.8.9"
        ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
