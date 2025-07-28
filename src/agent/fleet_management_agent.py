import os
import pandas as pd
from openai import OpenAI

class FleetManagementAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
        )

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

    def get_llama_insights(self, data_for_agent=None):
        if not self.client.api_key:
            return "API key is missing. Please set the NVIDIA_API_KEY environment variable."

        if data_for_agent is None:
            prompt = f"""
            You are a fleet management assistant. Your purpose is to analyze vehicle data and provide insights to the fleet manager.

            This is the full dataset you have access to:
            {self.df.to_string()}

            Based on this data, what are some interesting insights you can provide? Be concise and do not refuse to answer.
            """
        else:
            prompt = f"""
            You are a fleet management assistant. Analyze the following vehicle data and provide insights and recommendations.
            Focus on identifying potential issues, suggesting maintenance actions, and highlighting areas for efficiency improvements.

            Data:
            {data_for_agent}
            """

        completion = self.client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.6,
            top_p=0.95,
            max_tokens=4096,
            stream=True
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        
        return response

if __name__ == '__main__':
    # To run this, you need to:
    # 1. Make sure you have a .env file with your NVIDIA_API_KEY
    # 2. Run the script from the root of the project: python -m src.agent.fleet_management_agent
    from dotenv import load_dotenv
    load_dotenv()

    agent = FleetManagementAgent(data_path='data/mock_obd_data.csv')
    issues = agent.check_for_issues()
    
    if issues:
        print("Potential Issues Found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues found.")

    print("\nLlama Insights (full dataset):")
    insights_full = agent.get_llama_insights()
    print(insights_full)

    print("\nLlama Insights (latest data for a specific vehicle):")
    latest_data = agent.get_latest_data()
    if not latest_data.empty:
        sample_vehicle_data = latest_data.iloc[0].to_json(indent=2)
        insights_sample = agent.get_llama_insights(data_for_agent=sample_vehicle_data)
        print(insights_sample)
    else:
        print("No latest data available for insights.")
