from flask import Flask, request, jsonify
import os
import hmac
import hashlib

app = Flask(__name__)

# Retrieve GitHub webhook secret from environment variable
GITHUB_SECRET = os.getenv('GITHUB_SECRET')
PORT = os.getenv('PORT', 5000)

def verify_signature(request):
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route('/hooks/github/pull-request', methods=['POST'])
def handle_pull_request():
    if not verify_signature(request):
        return jsonify({'error': 'Invalid signature'}), 403

    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'pull_request':
        action = payload.get('action')
        pr_number = payload.get('number')
        title = payload.get('pull_request', {}).get('title')

        # Implement your logic here
        print(f"Pull Request #{pr_number} - {title} - Action: {action}")

        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'ignored'}), 200

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({'status': 'healthy'}), 200

@app.route('/ready', methods=['GET'])
def ready():
    return jsonify({'status': 'ready'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

