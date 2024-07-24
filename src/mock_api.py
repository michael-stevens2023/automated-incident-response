from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Simulate fetching a large number of logs with random timestamps.
    """
    logs = []
    num_logs = 100

    for _ in range(num_logs):
        log = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - random.randint(0, 3600))),
            "event_type": random.choice(["login", "file_access", "network"]),
            "result": random.choice(["success", "failure"]),
            "ip_address": f'192.168.1.{random.randint(1, 255)}'
        }
        logs.append(log)
    return jsonify(logs)

@app.route('/firewall', methods=["POST"])
def firewall():
    """
    Simulate sending a response to the firewall with random success or failure
    """
    data = request.json
    action = data.get('action')
    ip_address = data.get('ip_address')

    if action == 'block':
        #implement blocking logic here
        return jsonify({"status": "success", "message": f"IP {ip_address} blocked."})
    else:
        return jsonify({"status": "error", "message": "Invalid action."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
