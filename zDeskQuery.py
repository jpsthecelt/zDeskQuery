#!/usr/bin/python

import requests
import pprint
import argparse
import json

#
# This is a sample program intended to demonstrate querying information in ZenDesk
# it requires previously 'set up' access to ZenDesk (client_id and client_secret, etc)
#

# Set the request parameters
#url = 'https://your_subdomain.zendesk.com/api/v2/groups.json'
#user = 'your_email_address'
#pwd = 'your_password'
#
## Do the HTTP get request
#response = requests.get(url, auth=(user, pwd))
#
## Check for HTTP codes other than 200
#if response.status_code != 200:
#    print('Status:', response.status_code, 'Problem with the request. Exiting.')
#    exit()
#
## Decode the JSON response into a dictionary and use the data
#data = response.json()
#
## Example 1: Print the name of the first group in the list
#print( 'First group = ', data['groups'][0]['name'] )
#
## Example 2: Print the name of each group in the list
#group_list = data['groups']
#for group in group_list:
#    print(group['name'])
#

def queryZenDesk(cfgFilename, clientid, clientsecret, zenDeskUser, zenDeskPassword):
    # Set up JSON prettyPrinting
    pp = pprint.PrettyPrinter(indent=4)
    
    # Setup to obtain Get authorization-token
    authTokenUrl = "https://usoauth.plutora.com/oauth/token"
    payload = 'client_id=' + clientid + '&client_secret=' + clientsecret + '&grant_type=password&username='
    payload = payload + zenDeskUsername + '&password=' + zenDeskPassword + '&='
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
        }
    
    # Connect to get zenDesk access token for subsequent queries
    authResponse = requests.post(authTokenUrl, data=payload, headers=headers)
    if authResponse.status_code != 200:
        print('Get auth-release status code: %i' % authResponse.status_code)
        print('zDeskQuery.py: Sorry! - [failed on getAuthToken]: ', authResponse.text)
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        print('\nzDeskQuery.py - authTokenGet: ')
        pp.pprint(authResponse.json())
        accessToken = authResponse.json()["access_token"]
    
    # Setup to query Maersk zenDesk instances
    plutoraBaseUrl= 'https://usapi.plutora.com'
    plutoraMaerskUrl = r'http://maersk.plutora.com/changes/12/comments'
    plutoraMaerskTestUrl = r'https://usapi.plutora.com/me'
    #jiraURL = r'http://localhost:8080/rest/api/2/search?jql=project="DemoRevamp"&expand'
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': "bearer "+accessToken,
        'cache-control': "no-cache",
        'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
    }
    
    # Experiment -- Get zenDesk information for all system releases, or systems, or just the organization-tree
    getReleases = '/releases/9d18a2dc-b694-4b20-971f-4944420f4038'
    getSystems = '/systems'
    getOrganizationsTree = '/organizations/tree'
    
    r = requests.get(plutoraBaseUrl+getOrganizationsTree, data=payload, headers=headers)
    if r.status_code != 200:
        print('Get release status code: %i' % r.status_code)
        print('\npltSystemCreate.py: too bad sucka! - [failed on zenDesk get]')
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        print('\npltSystemCreate.py - zenDesk get of organizations information:')
        pp.pprint(r.json())
    
    # OK; try creating a new system...
    try:
        payload = """{ "additionalInformation": [{}], "name": "API created System 1", "vendor": "API created vendor", "status": "Active", "organizationId": "%s", "description": "Description of API created System 1" }""" % r.json()['childs'][0]['id']
    #"additionalInformation":[],
        
        postSystem = '/systems'
        print("Here's what I'm sending zenDesk (headers & payload):")
        print("header: ",headers)
        print("payload: ",payload)
        
        r = requests.post(plutoraBaseUrl+postSystem, data=payload, headers=headers)
        if r.status_code != 200:
            print('Post new system status code: %i' % r.status_code)
            print('\npltSystemCreate.py: too bad sucka! - [failed on zenDesk create system POST]')
            pp.pprint(r.json())
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            print('\npltSystemCreate.py - zenDesk POST of new system information:')
            pp.pprint(r.json())
    except Exception,ex:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: %s " % ex.msg
        exit('Error during API processing [POST]')
        
# Residual stuff follows:
#for i in r.json()["issues"]:
#    print("field is", i["fields"]["description"])
#    r = requests.post(plutoraMaerskUrl, data=i["fields"]["description"], headers=headers)
#    if r.status_code != 200:
#       print "Error inserting record into zenDesk:", i, r.status_code
#       exit('Cant insert into zenDesk')
#    else:
#       print('zDeskQuery.py: too bad sucka! - [failed on POST]')

if __name__ == '__main__':
    # parse commandline and get appropriate passwords
    #    accepted format is python zDeskQuery.py -f <config fiiename> -pusername:password
    #
    parser = argparse.ArgumentParser(description='Get user/password zenDesk and configuration-filename.')
    #   help='JIRA and zenDesk logins (username:password)')
    parser.add_argument('-f', action='store', dest='config_filename',
                        help='Config filename ')
    parser.add_argument('-p', action='store', dest='pltUnP',
                        help='zenDesk username:password')
    results = parser.parse_args()

    config_filename = results.config_filename.split(':')[0]
    plutora_username = results.pltUnP.split(':')[0].replace('@', '%40')
    plutora_password = results.pltUnP.split(':')[1]

    # If we don't specify a configfile on the commandline, assume one & try accessing
    if len(config_filename) <= 0:
        config_filename = 'syscreate.cfg'

    # using the specified/assumed configfilename, grab ClientId & Secret from manual setup of zenDesk Oauth authorization.
    try:
        with open(config_filename) as data_file:
            data = json.load(data_file)
        client_id = data["credentials"]["clientId"]
        client_secret = data["credentials"]["clientSecret"]
    except Exception,ex:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: %s " % ex.msg
        exit('couldnt open file {0}'.format(config_filename))

    queryZenDesk(config_filename, client_id, client_secret, plutora_username, plutora_password)

    print("\n\nWell, it seems we're all done here, boys; time to pack up and go home...")
