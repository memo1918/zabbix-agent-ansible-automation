import requests
import json

def createJsonMaker(name:str , ip:str, groupids:list[str], templateids:list[str], token:str) -> dict:
    """This function adds the given group and template id's to the json
    
    Args:
        name (str): The name of the host.
        ip (str): The IP address of the host.
        groupids (list): List of group IDs.
        templateids (list): List of template IDs.
        token (str): Authentication token.

    Returns:
        data: A dictionary with the given parameters.
    """
   
    data =  {"jsonrpc":"2.0","method":"host.create","params":{"host": name,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"groups":[],"templates":[]},"auth":token,"id":1}

    for gid in groupids:
        data['params']['groups'].append({"groupid": gid})
    for tid in templateids:
        data['params']['templates'].append({"templateid": tid})
        
    return data


FILENAME = "configIps.txt"
USER = ""
PASS = ""
AUTHTOKEN=""

GROUPIDs = []
TEMPLATEIDs = []
ipList = {}

#Reads the config and generated a dictionary to store the names and ips.
#Also reads and seperates the groupids and templateid into lists.         
with open(FILENAME) as file:
    for line in file: 
        line = line.strip().rstrip('\n')
        if line and not line.startswith("#"):        
            
            key, value = line.rstrip().split(":",1)
            if key == "groupids":
                GROUPIDs = value.split(",")
            elif key == "templateids":
                TEMPLATEIDs = value.split(",")
            else:
                ipList[key] = value
                

print("\nServer ip -- ",ipList["Server"])
ZABBIX_URL = 'http://{}/zabbix/api_jsonrpc.php'.format(ipList.pop("Server"))

print("These ip's will be added as host")
for ip in ipList.values(): print(ip)

print("Group ids --",','.join(GROUPIDs))
print("Template ids --",','.join(TEMPLATEIDs),"\n")
input("Press a button to continue...")

#Uncomment this block to use login with user and password instead of a token.

##Try-except for the requests module and in case of wrong server ip.
#try:
#    #Sends the post to login to zabbix and get a auth token.
#    loginData = {"jsonrpc":"2.0","method":"user.login","params":{"username":USER,"password":PASS},"id":1}
#    response = requests.post(ZABBIX_URL, json=loginData, headers={"Content-Type": "application/json-rpc"})
#except:
#    print("Requests module threw an exception. Please check the modeule and the " + "\u0332".join("server ip"))
#    exit()
#
##This if-else checks the response.
#if response.json()["result"]:
#    print("\n**Login successfull**")
#    print("Saving Auth Token\n")
#    AUTHTOKEN = response.json()["result"]
#else:
#    print("\n**!!Login Failed!!**\n")
#    print(response.json()["error"])
#    exit()


#This post gets all the host information from zabbix.
try:
    getHosts = {"jsonrpc":"2.0","method":"host.get","params":{"output":["hostid","host"],"selectInterfaces":["interfaceid","ip"]},"id":2,"auth":AUTHTOKEN}
    response = requests.post(ZABBIX_URL, json= getHosts )
except:
    print("Requests module threw an exception. Please check the modeule and the " + "\u0332".join("server ip"))
    exit()

if response.json()["result"]:
    print("**Auth successfull**\n")
else:
    print("**!!Auth Failed!!**\n")
    print(response.json()["error"])
    exit()

#We save the host ip's to a list
existingIps = []
for host in response.json()['result']:
    if host['host'] == "Zabbix server": continue
    for inter in host['interfaces']:
        existingIps.append(inter['ip'])
        
#We check if the new ip's are already in the zabbix by taking difference to host ips in zabbix.
differenceIps = set(ipList.values())-(set(existingIps))
difference_dict = {key: value for key, value in ipList.items() if value in differenceIps}

#We check if the difference results in empty dict or not
if difference_dict:
    #This loop generates posts based on the name and ip from difference_dict
    for name,ip in difference_dict.items():

        createData =  createJsonMaker(name,ip,GROUPIDs,TEMPLATEIDs,AUTHTOKEN)
            
        response = requests.post(ZABBIX_URL, json=createData )
        
        if response.json()["result"]:
            print("{} created!".format(name))
        else:
            print("Error on {}/{}".format(name,ip))
            print(response.json["error"])
                   
else:
    print("Hosts already exists.")
    
    

print("\n**END**")




        
