import pandas as pd

def load_ev_stations_data(csv_file_path):
    try:
        ev_data = pd.read_csv(csv_file_path)
        ev_data.columns = ev_data.columns.str.strip()
        ev_data.rename(columns={'Lattitude': 'Latitude'}, inplace=True)
        ev_data['Latitude'] = pd.to_numeric(ev_data['Latitude'], errors='coerce')
        ev_data['Longitude'] = pd.to_numeric(ev_data['Longitude'], errors='coerce')
        ev_data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
        return ev_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
