import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
NUM_VEHICLES = 10
DATA_POINTS = 100
VEHICLE_IDS = [f"Vehicle_{i+1}" for i in range(NUM_VEHICLES)]
DTC_CODES = ["P0301", "P0171", "P0420", "P0442", "P0135", "P0300", "P0455", "P0128", "P0401", "P0302"]

def generate_mock_data():
    data = []
    current_time = datetime.now()

    for _ in range(DATA_POINTS):
        for vehicle_id in VEHICLE_IDS:
            current_time += timedelta(seconds=10)
            data.append({
                "timestamp": current_time,
                "vehicle_id": vehicle_id,
                "engine_rpm": random.randint(800, 4000),
                "coolant_temp": random.randint(80, 105),
                "fuel_trim": random.uniform(-5, 5),
                "dtc": random.choice(DTC_CODES + [None]*20),  # 1 in 21 chance of a DTC
                "latitude": random.uniform(34.0, 34.1),
                "longitude": random.uniform(-118.3, -118.2),
                "tire_pressure": random.randint(28, 35)
            })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    mock_data = generate_mock_data()
    mock_data.to_csv("data/mock_obd_data.csv", index=False)
    print(f"Generated {len(mock_data)} data points and saved to data/mock_obd_data.csv")
