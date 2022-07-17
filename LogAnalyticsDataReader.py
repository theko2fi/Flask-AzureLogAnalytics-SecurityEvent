
import urllib3
import logging
import requests
import json

def get_token(tenant, sp_id, sp_secret):
    """Obtain authentication token using a Service Principal"""
    login_url = "https://login.microsoftonline.com/"+tenant+"/oauth2/token"
    resource = "https://api.loganalytics.io"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': sp_id,
        'client_secret': sp_secret,
        'Content-Type': 'x-www-form-urlencoded',
        'resource': resource
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.post(login_url, data=payload, verify=False)
        if (response.status_code >= 200 and response.status_code <= 299):
            logging.info('Token obtained')
            token = json.loads(response.content)["access_token"]
            return {"Authorization": str("Bearer "+ token), 'Content-Type': 'application/json'}
        else:
            logging.error("Unable to Read: " + format(response.status_code))
        
    except Exception as error:
        logging.error(error)


def get_data(query, token, azure_log_customer_id):
    
    """Executes a KQL on a Azure Log Analytics Workspace
    
    Keyword arguments:
    query -- Kusto query to execute on Azure Log Analytics
    token -- Authentication token generated using get_token
    azure_log_customer_id -- Workspace ID obtained from Advanced Settings
    """
    
    az_url = "https://api.loganalytics.io/v1/workspaces/"+ azure_log_customer_id + "/query"
    query = {"query": query}

    try:
        response = requests.get(az_url, params=query, headers=token)
        if (response.status_code >= 200 and response.status_code <= 299):
            logging.info('Query ran successfully')
            return json.loads(response.content)
        else:
            logging.error("Unable to Read: " + format(response.status_code))
    except Exception as error:
        logging.error(error)
    