import json
import base64
import requests

WEB_SERVER_URL = "http://3.86.82.237/update_position" #Public IP of Web-Server

def lambda_handler(event, context):
    for record in event['Records']:

        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)

        if 'position' not in data or data['position'] is None:
            continue
        
        driver = data.get('driver')
        position = data.get('position')
        team = data.get('team')
        lap_number = data.get('lap_number')
        tyre_age = data.get('tyre_age')
        tyre = data.get('tyre')

        if driver and position:
            try:
                position_data = {
                    'driver': driver,
                    'team': team,
                    'position': position,
                    'lap_number': lap_number,
                    'tyre': tyre,
                    'tyre_age': tyre_age
                }
                print(position_data)
                
                # Send the driver position data to the web server via HTTP POST
                response = requests.post(WEB_SERVER_URL, json=position_data)
                
                # Log the response from the server
                if response.status_code == 200:
                    print(f"Driver {driver}'s position sent successfully: {position}")
                else:
                    print(f"Failed to send driver {driver}'s position: {response.status_code}")
            except Exception as e:
                print(f"Error sending position data: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Driver position processed successfully!')
    }
