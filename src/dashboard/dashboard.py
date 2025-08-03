import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from agent.fleet_management_agent import FleetManagementAgent

load_dotenv()

st.set_page_config(layout="wide")

st.title("Fleet Management Dashboard")

# Load data
DATA_URL = "data/mock_obd_data.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


df = load_data()

# Get the latest data for each vehicle
latest_data = df.sort_values("timestamp").groupby("vehicle_id").last().reset_index()

st.sidebar.header("Vehicles")
selected_vehicle = st.sidebar.selectbox(
    "Select a Vehicle", latest_data["vehicle_id"].unique()
)

# Filter data for the selected vehicle
vehicle_data = df[df["vehicle_id"] == selected_vehicle]

# Display vehicle details
st.header(f"Vehicle: {selected_vehicle}")

# Display latest data in a more organized way
st.subheader("Latest Vehicle Status")
latest_vehicle_data = latest_data[latest_data["vehicle_id"] == selected_vehicle].iloc[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Engine RPM", latest_vehicle_data["engine_rpm"])
with col2:
    st.metric("Coolant Temp", f"{latest_vehicle_data['coolant_temp']} °C")
with col3:
    st.metric("Fuel Trim", f"{latest_vehicle_data['fuel_trim']:.2f}%")
with col4:
    st.metric("Tire Pressure", f"{latest_vehicle_data['tire_pressure']} PSI")

# Display DTC codes if any
if pd.notna(latest_vehicle_data["dtc"]):
    st.warning(f"DTC Code: {latest_vehicle_data['dtc']}")
else:
    st.success("No DTC Codes")

# Display historical data
st.subheader("Historical Data")
st.line_chart(
    vehicle_data.set_index("timestamp")[
        ["engine_rpm", "coolant_temp", "fuel_trim", "tire_pressure"]
    ]
)

# Display map
st.subheader("Vehicle Location")

# Get the latest location
map_data = latest_data[["vehicle_id", "latitude", "longitude"]].copy()
map_data.rename(columns={"latitude": "lat", "longitude": "lon"}, inplace=True)

# Create a map centered around the average location
center_lat = map_data["lat"].mean()
center_lon = map_data["lon"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add markers for each vehicle
for _, row in map_data.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]], popup=row["vehicle_id"], tooltip=row["vehicle_id"]
    ).add_to(m)

# Highlight the selected vehicle
selected_vehicle_location = map_data[map_data["vehicle_id"] == selected_vehicle]
if not selected_vehicle_location.empty:
    folium.Marker(
        [
            selected_vehicle_location.iloc[0]["lat"],
            selected_vehicle_location.iloc[0]["lon"],
        ],
        popup=selected_vehicle,
        tooltip=selected_vehicle,
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

# Display the map
st_folium(m, width=1200, height=600)

# Llama Agent Integration
st.subheader("Llama Agent Insights")

# Initialize the agent
agent = FleetManagementAgent(data_path=DATA_URL)

user_question = st.text_area(
    "Ask a question about the selected vehicle:",
    "What are the potential issues with this vehicle?",
)

if st.button("Get AI Feedback"):
    with st.spinner("Getting feedback from Llama Agent..."):
        # Prepare data for the agent
        data_for_agent = latest_vehicle_data.to_json(indent=2)

        insights = agent.get_llama_insights(data_for_agent, user_question)
        st.write(insights)

# Optional: Display raw data sent to agent for debugging
# with st.expander("View Raw Data Sent to Agent"):
#     st.json(latest_vehicle_data.to_dict())
