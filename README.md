# Azure Functions Sample in Python
Sample code showing how to set up Azure Functions using Python

## Overview
This code contains two functions: 
1. **GetAuth** - this simulates a call to an auth provider and returns an AuthCode that is then used in calls to the other function. It accepts a user and password as json in the body of the post. The auth code retrieved is from the configuration setting AuthCode (in the local.settings.json file when running locally and the AuthCode application setting when running in Azure)
1. **GetLogData** - this simulates retrieving log data. It will query CosmosDB for the records that are between two dates passed in as part of the URL. Format is `api/logs/{startDate}/{endDate}` It expects the auth code returned from GetAuth as a header.

There is a test harness `testharness.py` that can be used to show how the functions might be called. This code retrieves an auth token and uses it to call the GetLogs for a series of dates and then saves the files locally. When running against the functions in Azure, you need to modify the values for the baseUrl, and function auth codes. 

## Setup
1. Create Azure Function App 
1. Enable Managed Identity for Function App
1. Create Azure Key Vault
1. Give Function App's Managed Identity *Get* access to the Key Vault's secrets
1. Create Cosmos DB Account (SQL Driver)
1. Create a new database/container called funclogs/logs and then upload the *samplelogs.json* file into it
1. Add the connection string from Cosmos DB as secret in the Key Vault
1. Add another Key Vault secret called AuthCode and set the code used for authentication

## Running locally
1. Update the local.settings.json to the Cosmos DB connection string
1. Ensure the [Azure Functions CLI](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Ccsharp%2Cbash) is installed and logged into Azure
1. Open with VSCode - this should prompt to install the Azure Functions extention and set up the project for debugging
1. Hit play and verify using the two test URLs with curl:
    1. `curl --header "Content-Type: application/json" --request POST --data '{"user":"user1","password":"pass123"}' http://localhost:7071/api/GetAuth`
    1. `curl -H 'AuthCode: Abc123' http://localhost:7071/api/logs/2020-11-01/2020-11-15`

## Deploying Function to Azure
1. Create two application settings in the Function App pointing to the secrets in the Key Vault:
    1. AuthCode: @Microsoft.KeyVault(SecretUri=SECRET_URL)
    1. CosmosDBConnection: @Microsoft.KeyVault(SecretUri=COSMOS_SECRET_URL)
1. Deploy using the function CLI `func azure functionapp publish [FUNCTION_APP_NAME]`
1. When complete you will see the URL and function codes for the two function. Use these with CURL or in the top of the test harness file. 
