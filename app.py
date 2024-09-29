from flask import Flask, render_template

app = Flask(__name__)

@app.route('/ai-health', methods=['GET'])
def health_check():
    status = "healthy"
    message = "I'm healthy!!"
    return render_template('health_check.html', status=status, message=message)

if __name__ == '__main__':
    app.run()