import pandas as pd

class FleetAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

    def get_latest_data(self):
        return self.df.sort_values(by='timestamp', ascending=False).groupby('vehicle_id').first().reset_index()

    def check_for_issues(self):
        latest_data = self.get_latest_data()
        issues = []

        for _, row in latest_data.iterrows():
            # Check for DTC codes
            if pd.notna(row['dtc']):
                issues.append(f"Vehicle {row['vehicle_id']} has a DTC code: {row['dtc']}")
            
            # Check for low tire pressure
            if row['tire_pressure'] < 30:
                issues.append(f"Vehicle {row['vehicle_id']} has low tire pressure: {row['tire_pressure']} PSI")

            # Check for overheating
            if row['coolant_temp'] > 100:
                issues.append(f"Vehicle {row['vehicle_id']} is overheating: {row['coolant_temp']}°C")

        return issues

if __name__ == '__main__':
    agent = FleetAgent('data/mock_obd_data.csv')
    issues = agent.check_for_issues()
    
    if issues:
        print("Potential Issues Found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues found.")
