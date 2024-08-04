import requests
import json

reqUrl = "http://127.0.0.1:9100/"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "printer": "zebraa",
  "data": "^XA~JC^XZ"
})

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)