import json
import boto3
import base64

sns_client = boto3.client('sns', region_name='us-east-1')
FASTEST_LAP = None

def lambda_handler(event, context):
    global FASTEST_LAP
    for record in event['Records']:

        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)

        if 'lap_time' not in data or data['lap_time'] is None:
            continue
        
        try:
            lap_time = float(data['lap_time'])
        except (ValueError, TypeError):
            continue
        
        driver = data.get('driver')
        lap_number = data.get('lap_number')
        team = data.get('team')
        tyre = data.get('tyre')
        
        if FASTEST_LAP is None or lap_time < FASTEST_LAP['lap_time']:
            FASTEST_LAP = {
                'driver': driver,
                'team': team,
                'lap_time': lap_time,
                'lap_number': lap_number,
                'tyre': tyre
            }
            print(f"New fastest lap: {driver} - Lap {lap_number} - Time: {lap_time}")

            sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:843576970817:F1-Fastest-Lap',
                Message=json.dumps({
                    'event': 'Fastest Lap',
                    'driver': driver,
                    'team': team,
                    'lap_time': lap_time,
                    'lap_number': lap_number,
                    'tyre': tyre
                }),
                Subject='Fastest Lap Update'
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Fastest lap processed successfully!')
    }
