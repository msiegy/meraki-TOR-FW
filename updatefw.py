import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MerakiAPIKey = os.environ.get('MerakiAPIKey')
networkid = os.environ.get('networkid')
url = os.environ.get('url')

ipv4 = []

response = requests.get(url)
open("tornodes.json", "wb").write(response.content)

f = open ('tornodes.json', "r")
  
# Read TOR Guard Nodes from file and extract IPV4 only addresses
data = json.loads(f.read())

length = len(data['relays'])
i=0
while(i < length):
     #print(data['relays'][i]['or_addresses'][0])
     ipv4.append(data['relays'][i]['or_addresses'][0].split(":", 1)[0])
     i = i + 1 

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

#import ipdb
#ipdb.set_trace()
#print (payload)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": MerakiAPIKey
}

response = requests.request('PUT', url, headers=headers, data = payload)

print(response.text.encode('utf8'))
