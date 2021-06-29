import requests
import json
url = 'https://api.mist.com/api/v1/sites/:site_id/wlans'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token your_token'
}

results = requests.get(url, headers=headers)
wlans = json.loads(results.text)

for wlan in wlans:
    print(wlan["ssid"], ">", wlan["id"])
