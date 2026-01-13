import pandas as pd


## (Helper Function) Returns a dictionary (match_id_data) of NAMES from the corresponding MATCH_ID.
## Key: MATCH_ID (string). Value: NAMES as a tuple of strings: (Player 1, Player 2).

def getPlayersFromIds(matches_fileloc):
    matches = pd.read_csv(matches_fileloc)
    match_id_data = { }
    for _, row in matches.iterrows():
        p1 = row['player1']
        p2 = row['player2']
        id = row['match_id']
        match_id_data[id] = (p1, p2)
    return match_id_data
