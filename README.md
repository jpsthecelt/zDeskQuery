**`PURPOSE`**:
This is an example of how you would programmatically query ZenDesk
for information about particular customers, the intent of which is to provide a customer
analytics dashboard.

**`IMPLEMENTATION`**
Programmed in Python, using the requests library, this program
takes commandline parameters of the form 
    'python zDeskQuery.py -p username:password -f myzdcredentials.cfg'

The user/password parameters (as well as the authorization-code from the config-file) 
are then used to log into your Zendesk portal 

The 'API' parameters are contained in the file specified 
after the -f' commandline parameter, elsewise in a file in the local
directory named 'zdredentials.cfg'

	12.27.16-jps
