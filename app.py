from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for driver positions
driver_positions = []

@app.route('/')
def index():
    # Render the HTML with an empty driver_positions (JS will update it)
    return render_template('index.html')

@app.route('/positions')
def get_positions():
    # Return the driver positions as JSON, sorted by position
    return jsonify(sorted(driver_positions, key=lambda x: x['position']))

@app.route('/update_position', methods=['POST'])
def update_position():
    # Get the driver position data from the request
    data = request.get_json()

    # Update the driver positions list
    for position in driver_positions:
        if position['driver'] == data['driver']:
            # Update existing driver info
            position.update(data)
            break
    else:
        # If the driver does not exist, add a new entry
        driver_positions.append(data)

    return jsonify({'message': 'Driver position updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
