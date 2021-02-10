import logging
import os
import json
import azure.functions as func

def main(req: func.HttpRequest, logItems: func.DocumentList) -> func.HttpResponse:
    startdate = req.route_params.get('startdate')
    enddate = req.route_params.get('enddate')
    logging.info(f'Received log file request. Start Date: {startdate} End Date: {enddate}')

    # validate auth code from headers with authcode in app variables for function
    headerAuthCode = req.headers.get('AuthCode')
    authCode = os.environ["AuthCode"]
    if not authCode == headerAuthCode:
         return func.HttpResponse(
             "Unauthorized",
             status_code=403
        )

    # add items into list for seralization 
    body = []
    for item in logItems:
        body.append(item.data)
    logging.info(f"Returning {len(body)} items.")

    return func.HttpResponse(
            body=json.dumps(body),
            status_code=200
    )

    # To test: curl -H 'AuthCode: Abc123' http://localhost:7071/api/logs/2020-11-01/2020-11-15