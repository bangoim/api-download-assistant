import requests
import time
import os
import csv
import urllib3
from urllib.parse import urlparse

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define API key
apikey = "<Your API Key>"

# Define download directory
download_dir = "<Your Download Directory>"

# Define offset file
offset_file = os.path.join(download_dir, "last_offset.txt")

# Define failed offsets file
failed_offsets_file = os.path.join(download_dir, "failed_offsets.txt")

# Define methods
def lookup_player_by_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupPlayerById?apikey={apikey}&playerid={offset}&format=csv"

def lookup_player_tournaments(offset):
    return f"http://api.esportsearnings.com/v0/LookupPlayerTournaments?apikey={apikey}&playerid={offset}&offset={offset}&format=csv"

def lookup_highest_earning_players(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningPlayers?apikey={apikey}&offset={offset}&format=csv"

def lookup_game_by_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupGameById?apikey={apikey}&gameid={offset}&format=csv"

def lookup_highest_earning_players_by_game(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningPlayersByGame?apikey={apikey}&gameid={offset}&offset={offset}&format=csv"

def lookup_recent_tournaments(offset):
    return f"http://api.esportsearnings.com/v0/LookupRecentTournaments?apikey={apikey}&offset={offset}&format=csv"

def lookup_tournament_by_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupTournamentById?apikey={apikey}&tournamentid={offset}&format=csv"

def lookup_tournament_results_by_tournament_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupTournamentResultsByTournamentId?apikey={apikey}&tournamentid={offset}&format=csv"

def lookup_tournament_team_results_by_tournament_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupTournamentTeamResultsByTournamentId?apikey={apikey}&tournamentid={offset}&format=csv"

def lookup_tournament_team_players_by_tournament_id(offset):
    return f"http://api.esportsearnings.com/v0/LookupTournamentTeamPlayersByTournamentId?apikey={apikey}&tournamentid={offset}&format=csv"

def lookup_highest_earning_teams(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningTeams?apikey={apikey}&offset={offset}&format=csv"

def lookup_highest_earning_teams_by_game(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningTeamsByGame?apikey={apikey}&gameid={offset}&offset={offset}&format=csv"

# Define methods dictionary
methods = {
    1: lookup_player_by_id,
    2: lookup_player_tournaments,
    3: lookup_highest_earning_players,
    4: lookup_game_by_id,
    5: lookup_highest_earning_players_by_game,
    6: lookup_recent_tournaments,
    7: lookup_tournament_by_id,
    8: lookup_tournament_results_by_tournament_id,
    9: lookup_tournament_team_results_by_tournament_id,
    10: lookup_tournament_team_players_by_tournament_id,
    11: lookup_highest_earning_teams,
    12: lookup_highest_earning_teams_by_game
}

# Define method to download data
def download_data(url):
    try:
        # Send request
        response = requests.get(url, verify=False)

        # Check response status
        if response.status_code == 200:
            # Handle non-ASCII characters
            return response.content.decode('utf-8', errors='replace')
        else:
            print(f"Failed to download data for url {url}.")
            with open(failed_offsets_file, "a") as f:
                f.write(url + "\n")
            return None
    except Exception as e:
        print(f"Exception occurred while downloading data for url {url}: {e}")
        with open(failed_offsets_file, "a") as f:
            f.write(url + "\n")
        return None

# Define method to save data
def save_data(data, file_name):
    with open(file_name, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.splitlines())
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            next(reader)  # skip header
        for row in reader:
            writer.writerow(row)

# Define method to get last offset
def get_last_offset(method_number):
    if os.path.exists(offset_file):
        with open(offset_file, "r") as f:
            return int(f.read().strip())
    else:
        # Return 1000 if the method requires the playerid parameter
        if method_number in [1, 2]:
            return 1000
        else:
            return 0    

# Define method to set last offset
def set_last_offset(offset):
    with open(offset_file, "w") as f:
        f.write(str(offset))

# Define method to get method number
def get_method_number():
    print("Please select a method number:")
    for key, value in methods.items():
        print(f"{key}: {value.__name__}")
    return int(input("Method number: "))

# Define main function
def main():
    # Get method number
    method_number = get_method_number()

    # Get last offset
    last_offset = get_last_offset(method_number)

    # Initialize offset
    offset = last_offset

    # Initialize failed offsets
    failed_offsets = []

    # Loop until no more data
    while True:
        # Get URL
        url = methods[method_number](offset)

        # Download data
        print(f"Downloading data for offset {offset}...")
        data = download_data(url)

        # Check if data is not None
        if data is not None:
            # Get file name
            base_url = urlparse(url).netloc
            file_name = os.path.join(download_dir, base_url + ".csv")

            # Save data
            save_data(data, file_name)

            # Set last offset
            set_last_offset(offset)

            # Increment offset
            if method_number in [1, 2, 4, 7]:
                offset += 1
            else:
                offset += 100

            # Delay
            time.sleep(3)
        else:
            break

    # Print completion message
    if len(failed_offsets) > 0:
        print("Download completed. But not every offset could be downloaded.")
        print("Failed to download the following offsets: ", failed_offsets)
    else:
        print("Download completed.")

# Run main function
if __name__ == "__main__":
    main()
