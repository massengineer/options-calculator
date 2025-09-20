from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    sample_data = {
        "message": "Hello, World!",
        "items": [1, 2, 3, 4, 5]
    }
    return jsonify(sample_data)
  
if __name__ == '__main__':
    app.run(debug=True)