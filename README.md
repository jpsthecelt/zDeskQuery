**`PURPOSE`**:
This is an example of how you would programmatically query ZenDesk
for information about particular customers.

**`IMPLEMENTATION`**
Programmed in Python, using the requests library, this program
takes commandline parameters of the form 
    'python plSystemCreate.py -p username:password -f mysyscreate.cfg'

The user/password parameterws are then used to log into the specific Plutora 
instance associated with your login.

The 'system' parameters are contained in the file specified 
after the -f' commandline parameter, elsewise in a file in the local
directory named 'syscreate.cfg'

	12.23.16-jps
