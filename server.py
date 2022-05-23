from flask import Flask
from flask import request
from flask import send_from_directory, jsonify
import predictor
import os


p = predictor.Predictor()
app = Flask(__name__)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")


@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory("dist/", 'index.html')


@app.route('/getRecommendation', methods=['POST'])
def recommend():
    data = request.get_json(force=True)
    x = data.get("x")
    y = data.get("y")
    date = data.get("date")
    
    # print(data)
    date = date.split("/")
    date = f"{date[2]}/{date[1]}/{date[0]}"
    prediction = p.predict(str(date), (x, y))
    # print(prediction)
    return jsonify(prediction), 200


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(root, path)


if __name__ == '__main__':
    app.run(debug=True)