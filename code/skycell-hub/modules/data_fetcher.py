import json

def get_latest_data():
    # Replace with real data parsing or socket connection
    with open('data/balloon_state.json', 'r') as f:
        return json.load(f)
