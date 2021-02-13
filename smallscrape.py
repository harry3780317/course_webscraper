import requests
from requests.exceptions import HTTPError,Timeout

## params = year/term/dept/search_param

MATCH_LIST = ["fall","spring","summer"]
##input("list out courses format: year/<fall|spring|summer> \n or search course format: year/<fall|spring|summer>/search_wildcard")
def checkInputParams():
    while True:
        input_params = "2019/fall/eng" ## for testing purpose, please change to user input 
        if input_params:
            parse_in = input_params.split("/")
            if len(parse_in)< 2:
                continue

            if not parse_in[0].isnumeric or parse_in[1].lower() not in MATCH_LIST:
                continue
            query_str = "http://www.sfu.ca/bin/wcm/course-outlines?year={}&term={}".format(parse_in[0], parse_in[1].lower())
            if len(parse_in) == 3:
                query_str += "&search={}".format(parse_in[2])
            getResp(query_str)
            break
        
        
        
def getResp(query_str):
    try:
        res = requests.get(query_str,timeout=5)
        res.raise_for_status()
        jsonRes = res.json()
        print("FULL RESPONSE\n\n")
        print(jsonRes)
        print("\n\nONLY GET VALUE\n\n")
        for value in jsonRes:
            print(value["value"])

    except HTTPError as httperror:
            print(f"http error raised: code: {httperror}")
    except Timeout as timeout:
            print(f"http error timed out: code: {timeout}")
    except Exception as excep:
            print(f"exception raised: code: {excep}")
            
