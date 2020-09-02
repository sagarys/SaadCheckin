import requests
import sys
import pprint
import subprocess
import os
SAAD = "https://saad-ba.efi.com"

if len(sys.argv) == 2 :
    issue_id =sys.argv[1]    
else :
    print("Please pass the FITID ")    
    sys.exit(2)
    
def handle_response_errors(response):
    if response.status_code == 404:
        print("Not Found")
        sys.exit(404)

    if response.status_code == 401:
        print("Access Denied")
        sys.exit(401)

    if response.status_code != 200:
        print("Unhandled error: {}".format(response.status_code))
        sys.exit(response.status_code)
productDetailsJson = {
    "productName"           : "",
    "oem"                   : "",
    "configspec"            : ""
}
headers = {
    'Accept': 'application/json',
    'jira-login' : '',
    'jira-password' : '',
    'saad-api-key' : 'c0a109c2-9c81-4412-8ce8-55e743fe8215',
}
issue_url = "{saad}/api/v0/issues/{issue_id}".format(saad=SAAD, issue_id=issue_id)
response = requests.get(issue_url, headers=headers)
issue_dict = response.json()

issue_url = "{saad}/api/v0/issues/{issue_id}".format(saad=SAAD, issue_id=issue_id)
response = requests.get(issue_url, headers=headers)
issue_dict = response.json()

project_url = issue_dict['project']['url']
response = requests.get(project_url, headers=headers)
handle_response_errors(response)
project_dict = response.json()
productDetailsJson['productName'] = project_dict['name']
productDetailsJson['oem'] = project_dict['oem']
# - configspec
configspec_url = project_url + "configspec/"
response = requests.get(configspec_url, headers=headers)
handle_response_errors(response)
productDetailsJson['configspec'] = response.text
print(productDetailsJson)
# print(response.text)
