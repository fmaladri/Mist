import requests
import json
url = 'https://api.mist.com//api/v1/orgs/:org_id/networktemplates'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token your_token'
}

results = requests.get(url, headers=headers)
network_templates = json.loads(results.text)

for network_template in network_templates:
    {
        print("------"),
        print("Name: ", network_template["name"]),
        print("NTP Servers: ", network_template["ntp_servers"]),
        print("Id: ", network_template["org_id"]),
        print("------")
    }

change_ntp_severs = input("Do you want to change NTP servers? (Y)es or N(o): ")
if(change_ntp_severs == "Y"):
    ntp_severs = input("What is the address or FQDN of your NTP servers? :")
    payload = "{\n    \"ntp_servers\": \""+ntp_severs+"\"\n}"
    print(payload)
    url = url+'/'+network_template["org_id"]
    print(url)
    results = requests.request("PUT", url, headers=headers)
    print(results.text)
    results = requests.get(url, headers=headers)
    network_templates = json.loads(results.text)
    for network_template in network_templates:
        {
            print("------"),
            print("Name: ", network_template["name"]),
            print("NTP Servers: ", network_template["ntp_servers"]),
            print("Id: ", network_template["org_id"]),
            print("------")
        }
elif(change_ntp_severs == "N"):
    exit(0)
else:
    print("Your answer is incorrect")
