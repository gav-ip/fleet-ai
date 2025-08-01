import os
import smartcar
from openai import OpenAI

class FleetManagementAgent:
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
        )

    def get_vehicle_data(self):
        vehicle_ids = smartcar.get_vehicle_ids(self.access_token)['vehicles']
        vehicle = smartcar.Vehicle(vehicle_ids[0], self.access_token)
        attributes = vehicle.attributes()
        return attributes

    def get_llama_insights(self, user_question):
        if not self.client.api_key:
            return "API key is missing. Please set the NVIDIA_API_KEY environment variable."

        vehicle_data = self.get_vehicle_data()

        prompt = f"""
        You are a fleet management assistant. Analyze the following vehicle data and provide insights and recommendations.
        Focus on identifying potential issues, suggesting maintenance actions, and highlighting areas for efficiency improvements.

        Data:
        {vehicle_data}

        User Question: {user_question}
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