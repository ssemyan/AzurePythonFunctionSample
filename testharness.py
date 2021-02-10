import json
import requests as req

# Localhost
baseUrl = "http://localhost:7071/api/"

# Azure
baseUrl = "azureurl"
getAuthCode = "?code"
getLogsCode = "?code"

body= { 
     "user": "user1", 
     "password": "pass123" }

headers= {'Content-Type':'application/json'}

def checkResponse(response):
    if not response.status_code == 200:
        raise Exception(f"Bad request. Status code {response.status_code}")

def auth(): #authentication to get header code for subsequent requests
    url = baseUrl + "GetAuth" + getAuthCode
    response = req.post(url, headers=headers, json=body)

    checkResponse(response)

    authObj = response.json()    
    authCode = authObj['AuthCode']
    if not authCode:
        raise Exception("Did not obtain auth code")

    return authObj['AuthCode']

def ageing(date1, date2):
    
    url = baseUrl + "logs/" + date1 + "/" + date2 + getLogsCode
        
    print(f"Pulling report for {date1} to {date2}...", end='')

    response = req.get(url,headers=headers)
    checkResponse(response)
    
    json_data = response.json()
    
    file_string = 'LogFile_' + date1 + '.json'
    
    with open(file_string,'w') as json_file: 
        json.dump(json_data, json_file)

    print(f"done. File written to {file_string}")
        
# Get auth code and add to headers
authCode = auth()
headers['AuthCode'] = authCode 

date_arr = ['2020-11-01','2020-11-15','2020-12-01','2020-12-15','2021-01-01']

for i in range(len(date_arr)): 
    if i != len(date_arr)-1:
        ageing(date_arr[i],date_arr[i+1])
