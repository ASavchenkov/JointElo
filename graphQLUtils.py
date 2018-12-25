import requests
import json
from token_file import tok

def make_query(query_string,variables):


    headers = {"Authorization" : tok}
    payload = {
        "query" : query_string,
        "variables" : json.dumps(variables)
    }
    response = requests.post("https://api.smash.gg/gql/alpha", json = payload, headers = headers)
    return response


