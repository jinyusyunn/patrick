# server.py
from flask import Flask, request, jsonify
from patrick_method import patrick_minimize, multi_output_minimize

app = Flask(__name__)


@app.route('/minimize', methods=['POST'])
def minimize():
    data = request.json
    pis = data['pis']
    outputs = data['outputs']

    if len(outputs) == 1:
        out_name = list(outputs.keys())[0]
        result = {out_name: patrick_minimize(pis, outputs[out_name])}
    else:
        result = multi_output_minimize(pis, outputs)

    return jsonify(result)

app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

