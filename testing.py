import os
import time
import requests
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

apikey = "7ccb2bf499c272fc4c3995ce7be04e772ab97c5677e184a426e2d94e2400420a"
directory = "C:\\Users\\joaoc\\OneDrive\\Área de Trabalho\\eSports Project\\"
os.makedirs(directory, exist_ok=True)

option = int(input("Select an option:\n1. LookupHighestEarningPlayers\n2. LookupPlayerById\n"))
if option == 1:
    base_url = "http://api.esportsearnings.com/v0/LookupHighestEarningPlayers"
    increment = 100
elif option == 2:
    base_url = "http://api.esportsearnings.com/v0/LookupPlayerById"
    increment = 1
else:
    print("Invalid option.")
    exit()

last_offset_file = os.path.join(directory, "last_offset.txt")
output_file = os.path.join(directory, base_url.split("/")[-1] + ".csv")

failed_offsets = []

if os.path.exists(last_offset_file):
    with open(last_offset_file, "r") as file:
        offset = int(file.read()) + increment
else:
    offset = 0 if option == 1 else 1000

while True:
    url = f"{base_url}?apikey={apikey}&offset={offset}&format=csv" if option == 1 else f"{base_url}?apikey={apikey}&playerid={offset}&format=csv"

    try:
        response = requests.get(url, verify=False)
        if response.status_code != 200 or not response.text.strip():
            break
        temp_file = os.path.join(directory, f"temp_{offset}.csv")
        with open(temp_file, "w", encoding='utf-8') as file:
            file.write(response.text)

        df = pd.read_csv(temp_file)

        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df.to_csv(output_file, mode='w', index=False)

        os.remove(temp_file)

        print(f"Downloaded offset: {offset}")

        with open(last_offset_file, "w") as file:
            file.write(str(offset))

    except Exception as e:
        print(f"Failed to download offset: {offset}")
        failed_offsets.append(offset)

    offset += increment
    time.sleep(3)

if failed_offsets:
    print("Download completed. But not every offset could be downloaded.")
    print("Failed to download the following offsets: ", failed_offsets)
else:
    print("Download completed.")
