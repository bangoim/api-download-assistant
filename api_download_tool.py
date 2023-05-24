import os
import time
import requests
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
base_url = "url_here"
apikey = "<api_key>"
directory = "<directory_here>"

os.makedirs(directory, exist_ok=True)
last_offset_file = os.path.join(directory, "last_offset.txt")
if os.path.exists(last_offset_file):
    with open(last_offset_file, "r") as file:
        offset = int(file.read())
else:
    offset = 0
output_file = os.path.join(directory, base_url.split("/")[-1] + ".csv")
while True:
    url = f"{base_url}?apikey={apikey}&offset={offset}&format=csv"
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

    offset += 100
    time.sleep(3)
