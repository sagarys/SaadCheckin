#!/usr/bin/env python
import os
import requests
import sys
import pprint
import subprocess
import json

if len(sys.argv) == 3 :
    SAAD =sys.argv[1]
    prodName = sys.argv[2]
else :
    print("Please pass the saad url and the project name ")
    sys.exit(2)

def handle_response_errors(response):
    if response.status_code == 404:
        print("Not Found\n")
        sys.exit(404)

    if response.status_code == 401:
        print("Access Denied\n")
        sys.exit(401)

    if response.status_code != 200:
        print("Unhandled error: {}".format(response.status_code))
        sys.exit(response.status_code)

headers = {
    'Accept': 'application/json',
    'jira-login' : '',
    'jira-password' : '',
    'saad-api-key' : 'c0a109c2-9c81-4412-8ce8-55e743fe8215',
}

projects_url = "{saad}/api/v0/projects/".format(saad=SAAD)
projects_url_configspec = "{saad}/api/v0/projects/".format(saad=SAAD)

response = requests.get(projects_url, headers=headers)
projects = response.json()

prod_configpsec = " "
key = " "
calculus_name = " "
project_name = " "
req  = 0

for project_dict in projects:        
    if str("{name}".format(**project_dict)) == prodName :
        prod_configpsec = "{saad}/api/v0/projects/".format(saad=SAAD)+str("{key}".format(**project_dict))+"/configspec"    
        response = requests.get(prod_configpsec, headers=headers)
        if response.status_code != 200 :
            print("Error Configspec not found for the product " + key + " with response status code "  + str(response.status_code))
        else :            
            configspec_path = "configspec.txt"
            if os.path.isfile(configspec_path):
                os.remove(configspec_path)
            f = open("configspec.txt", "w")
            f.write(response.text)
            f.close()            
