import logging
import os
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Received auth request.')

    validLogin = False
    try:
        req_body = req.get_json()
    except ValueError:
        logging.info("Could not get json body")
        pass
    else:
        user = req_body.get('user')
        password = req_body.get('password')
        # simulate logging into an auth provider
        if (user == "user1" and password == "pass123"):
            validLogin = True
        else:
            logging.info("Invalid username or password")

    if not validLogin:
        return func.HttpResponse(
             "Unauthorized",
             status_code=403
        )

    # Valid - return auth code to use for subsequent requests
    authCode = os.environ["AuthCode"]
    return func.HttpResponse(json.dumps({'AuthCode': authCode}))

# To test: curl --header "Content-Type: application/json" --request POST --data '{"user":"user1","password":"pass123"}' http://localhost:7071/api/GetAuth