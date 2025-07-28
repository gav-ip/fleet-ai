# Fleet Management AI Agent

This project is a simple AI agent that monitors a fleet of vehicles and detects potential issues using Nvidia Nemo NIM.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Generate mock data:**
    ```bash
    python3 -m src.simulation.data_generator
    ```

2.  **Run the agent to check for issues:**
    ```bash
    python3 -m src.agent.fleet_management_agent
    ```

3.  **Run the dashboard:**
    ```bash
    streamlit run src/dashboard/app.py
    ```

## Project Structure

-   `data/`: Contains the mock data for the vehicles.
-   `src/`:
    -   `agent/`: Contains the AI agent logic.
    -   `dashboard/`: Contains the Streamlit dashboard application.
    -   `simulation/`: Contains the data generation script.
    -   `utils/`: Contains utility functions (currently empty).
-   `.gitignore`: Specifies which files to ignore in Git.
-   `README.md`: This file.
-   `requirements.txt`: Lists the Python dependencies.
