import json

def get_latest_data():
    # Replace with real data parsing or socket connection
    with open('data/balloon_state.json', 'r') as f:
        return json.load(f)
# This function should be replaced with the actual data fetching logic
# This is NOT the file that should be recieving and converting the data, 
# it should just be the one that loads the data in the proper format and dumps it into
# the balloon_state.json file