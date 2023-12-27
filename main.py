import pandas as pd
from player import Player
from utils import to_set, get_rarity
from evo import curr_evos  # List of current evolutions in the game

if __name__ == '__main__':
    # Import DataFrame
    df = pd.read_csv('eafc_players_final.csv')
    df.fillna('None', inplace=True)  # Fix nan in df (mostly for PlaystylePlus)

    player_set = set()  # Init set of evolved players

    # Choose evolutions for player search
    # evo_list = [evolution for evolution in curr_evos if evolution.name == 'Midfield Dynasty']
    evo_list = curr_evos  # In case all evolutions are wanted to search in

    # Run over df rows, each row create player and check evo_paths
    for i in range(df.shape[0]):
        row = df.iloc[i].tolist()  # Convert row to list
        player = Player(row[0], row[1], row[2], row[3], row[4], row[5], row[6],  # Create player object
                        row[7], row[8], row[9], to_set(row[10]), row[11], to_set(row[12]),
                        row[13], row[14], get_rarity(row[7]), list())

        player.update_evo_paths(player_set, evo_list, min_skills=5, min_wf=5)  # Specify conditions

    for p in player_set:
        print(p)
    print(f"The number of players found: {len(player_set)}")

