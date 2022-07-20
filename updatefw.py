import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MerakiAPIKey = os.environ.get('MerakiAPIKey')
networkid = os.environ.get('networkid')
nodesurl = os.environ.get('nodesurl')

ipv4 = []

print("Pulling down TOR Guard node list\n")
response = requests.get(nodesurl)
open("tornodes.json", "wb").write(response.content)

f = open ('tornodes.json', "r")
  
# Read TOR Guard Nodes from file and extract IPV4 only addresses
print("Reading list and formatting for Meraki FW rules\n")
data = json.loads(f.read())

for item in data['relays']:
     #print(data['relays'][i]['or_addresses'][0])
     ipv4.append(item['or_addresses'][0].split(":", 1)[0])

#convert list to string, keeping commas and removing quotes.
addresses= ",".join(ipv4)

url = "https://api.meraki.com/api/v1/networks/"+networkid+"/appliance/firewall/l3FirewallRules"

payload = '''{
    "rules": [
        {
            "comment": "Block TOR Guard Nodes.",
            "policy": "deny",
            "protocol": "tcp",
            "destPort": "any",
            "destCidr": "'''+addresses+'''",
            "srcPort": "Any",
            "srcCidr": "Any",
            "syslogEnabled": false
        }
    ]
}'''

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": MerakiAPIKey
}

print("Updating L3 FW rules for network: ", networkid, "\n")
response = requests.request('PUT', url, headers=headers, data = payload)

print(response.text.encode('utf8'))
print("\n", len(ipv4), " MX FW rules updated\n")
