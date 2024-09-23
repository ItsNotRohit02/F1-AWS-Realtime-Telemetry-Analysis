import time
import boto3
import json
import fastf1
import pandas as pd

kinesis_client = boto3.client('kinesis', region_name='us-east-1')

def send_to_kinesis(data, lap):
    kinesis_client.put_record(
        StreamName='F1RaceStream',
        Data=json.dumps(data),
        PartitionKey=f'Lap: {lap}'
    )

session = fastf1.get_session(2024, 'Silverstone', 'Race')
session.load()

laps = session.laps

laps_by_lap_number = laps.groupby('LapNumber')

def simulate_race():
    for lap_number, lap_group in laps_by_lap_number:
        for lap in lap_group.itertuples():
            lap_data = {
                'lap_number': lap.LapNumber,
                'driver': lap.Driver,
                'team': lap.Team,
                'position': lap.Position,
                'lap_time': lap.LapTime.total_seconds() if pd.notna(lap.LapTime) else None,
                'tyre': lap.Compound,
                'tyre_age': lap.TyreLife,
                'sector1': lap.Sector1Time.total_seconds() if pd.notna(lap.Sector1Time) else None,
                'sector2': lap.Sector2Time.total_seconds() if pd.notna(lap.Sector2Time) else None,
                'sector3': lap.Sector3Time.total_seconds() if pd.notna(lap.Sector3Time) else None,
            }
            print(lap_data)
            send_to_kinesis(lap_data, lap.LapNumber)
        
        # Simulate real-time delay (lap time / 10 for 10x speed)
        lap_times = [lap.LapTime.total_seconds() for lap in lap_group.itertuples() if pd.notna(lap.LapTime)]
        if lap_times:
            avg_lap_time = sum(lap_times) / len(lap_times)
            time.sleep(avg_lap_time / 10)

if __name__ == "__main__":
    print("Simulating F1 Race at 10x speed...")
    simulate_race()
    print("Race simulation complete.")



# Pandas(Index=0, Time=Timedelta('0 days 01:03:46.185000'), Driver='VER', DriverNumber='1', 
# LapTime=Timedelta('0 days 00:01:37.167000'), LapNumber=1.0, Stint=1.0, PitOutTime=NaT, 
# PitInTime=NaT, Sector1Time=NaT, Sector2Time=Timedelta('0 days 00:00:38.051000'), 
# Sector3Time=Timedelta('0 days 00:00:26.073000'), Sector1SessionTime=NaT, 
# Sector2SessionTime=Timedelta('0 days 01:03:20.151000'), Sector3SessionTime=Timedelta('0 days 01:03:46.213000'), 
# SpeedI1=300.0, SpeedI2=254.0, SpeedFL=246.0, SpeedST=296.0, IsPersonalBest=False, Compound='MEDIUM', TyreLife=1.0, 
# FreshTyre=True, Team='Red Bull Racing', LapStartTime=Timedelta('0 days 01:02:08.731000'), 
# LapStartDate=Timestamp('2023-07-09 14:03:09.767000'), TrackStatus='1', Position=2.0, Deleted=False, DeletedReason='', 
# FastF1Generated=False, IsAccurate=False)