from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ai-health', methods=['GET'])
def health_check():
    return jsonify(status='healthy', message='Im healthy!!'), 200

if __name__ == '__main__':
    app.run()