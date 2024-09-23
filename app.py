from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

driver_positions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/positions')
def get_positions():
    return jsonify(sorted(driver_positions, key=lambda x: x['position']))

@app.route('/update_position', methods=['POST'])
def update_position():
    data = request.get_json()

    for position in driver_positions:
        if position['driver'] == data['driver']:
            position.update(data)
            break
    else:
        driver_positions.append(data)

    return jsonify({'message': 'Driver position updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
