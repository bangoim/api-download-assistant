import requests
import time
import os
import csv
import urllib3
from urllib.parse import urlparse

os.system('cls')

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define download directory
download_dir = "<download_dir_here>"

# Define offset file
offset_file = os.path.join(download_dir, "last_offset.txt")

# Define rg file
rg_file = os.path.join(download_dir, "last_rg.txt")

# Define failed offsets file
failed_offsets_file = os.path.join(download_dir, "failed_offsets.txt")

# Define failed rg file
failed_rg_file = os.path.join(download_dir, "failed_rg.txt")

# Define methods
def lookup_player_by_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupPlayerById?apikey={apikey}&playerid={rg}&format=csv"

def lookup_player_tournaments(rg, offset):
    return f"http://api.esportsearnings.com/v0/LookupPlayerTournaments?apikey={apikey}&playerid={rg}&offset={offset}&format=csv"

def lookup_highest_earning_players(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningPlayers?apikey={apikey}&offset={offset}&format=csv"

def lookup_game_by_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupGameById?apikey={apikey}&gameid={rg}&format=csv"

def lookup_highest_earning_players_by_game(rg, offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningPlayersByGame?apikey={apikey}&gameid={rg}&offset={offset}&format=csv"

def lookup_recent_tournaments(offset):
    return f"http://api.esportsearnings.com/v0/LookupRecentTournaments?apikey={apikey}&offset={offset}&format=csv"

def lookup_tournament_by_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupTournamentById?apikey={apikey}&tournamentid={rg}&format=csv"

def lookup_tournament_results_by_tournament_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupTournamentResultsByTournamentId?apikey={apikey}&tournamentid={rg}&format=csv"

def lookup_tournament_team_results_by_tournament_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupTournamentTeamResultsByTournamentId?apikey={apikey}&tournamentid={rg}&format=csv"

def lookup_tournament_team_players_by_tournament_id(rg):
    return f"http://api.esportsearnings.com/v0/LookupTournamentTeamPlayersByTournamentId?apikey={apikey}&tournamentid={rg}&format=csv"

def lookup_highest_earning_teams(offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningTeams?apikey={apikey}&offset={offset}&format=csv"

def lookup_highest_earning_teams_by_game(rg, offset):
    return f"http://api.esportsearnings.com/v0/LookupHighestEarningTeamsByGame?apikey={apikey}&gameid={rg}&offset={offset}&format=csv"

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
def download_data(url, offset, rg):
    try:
        # Send request
        response = requests.get(url, verify=False)

        # Check response status
        if response.status_code == 200:
            # Handle non-ASCII characters
            return response.content.decode('utf-8', errors='replace')
        else:
            print(f"Failed to download data for url {url}.")
            if offset is not None:
                with open(failed_offsets_file, "a") as f:
                    f.write(str(offset) + "\n")
            if rg is not None:
                with open(failed_rg_file, "a") as f:
                    f.write(str(rg) + "\n")
            return None
    except Exception as e:
        print(f"Exception occurred while downloading data for url {url}: {e}")
        if offset is not None:
            with open(failed_offsets_file, "a") as f:
                f.write(str(offset) + "\n")
        if rg is not None:
            with open(failed_rg_file, "a") as f:
                f.write(str(rg) + "\n")
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

# Define method to get last offset and rg
def get_last_offset_and_rg(method_number):
    if os.path.exists(offset_file):
        with open(offset_file, "r") as f:
            last_offset = int(f.readline().strip())
    else:
        last_offset = 0 if method_number not in [1, 2] else 1000

    if os.path.exists(rg_file):
        with open(rg_file, "r") as f:
            last_rg = int(f.readline().strip())
    else:
        last_rg = 0 if method_number not in [1, 2, 4, 7] else 1000

    return last_offset, last_rg

# Define method to set last offset and rg
def set_last_offset_and_rg(offset, rg):
    with open(offset_file, "w") as f:
        f.write(str(offset))
    with open(rg_file, "w") as f:
        f.write(str(rg))


# Define method to get method number
def get_method_number():
    print("\nPlease select a method number:")
    for key, value in methods.items():
        print(f"{key}: {value.__name__}")
    return int(input("Method number: "))

# Define main function
def main():
    # Get API key
    global apikey
    apikey = input("Please enter your API key: ")

    # Get method number
    method_number = get_method_number()

    # Get last offset and rg
    last_offset, last_rg = get_last_offset_and_rg(method_number)

    # Initialize offset and rg
    offset = last_offset
    rg = last_rg

    # Loop until no more data
    while True:
        # Get URL
        print('')
        if method_number in [1, 2, 4, 7]:
            url = methods[method_number](rg)
            print(f"Downloading data for rg {rg}...")
        elif method_number in [3, 6, 11]:
            url = methods[method_number](offset)
            print(f"Downloading data for offset {offset}...")
        else:
            url = methods[method_number](offset, rg)
            print(f"Downloading data for offset {offset} and rg {rg}...")

        # Download data
        data = download_data(url, offset, rg)

        # Check if data is not None
        if data is not None:
            # Get file name
            base_url = urlparse(url).netloc
            file_name = os.path.join(download_dir, base_url + ".csv")

            # Save data
            save_data(data, file_name)

            # Set last offset and rg
            set_last_offset_and_rg(offset, rg)

            # Increment offset and rg
            if method_number in [1, 2, 4, 7]:
                rg += 1
            elif method_number in [3, 6, 11]:
                offset += 100
            else:
                offset += 100
                rg += 1

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
