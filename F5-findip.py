import sys, requests
from requests.auth import HTTPBasicAuth

username = "admin"
password = "password"

#f5dev.txt contains the IP address of the F5 devices
host_file = open("f5dev.txt","r").read().split('\n')

#ipchec.txt contains the list of pool IP to check
check_ip = open("ipcheck.txt","r").read().split('\n')

for ip in host_file:
    BASE_URL = "https://"+ip+"/mgmt/tm"
    if not ip:
        sys.exit()
    
    def makeRequest(username, password, url):
        response_data = requests.get(url, auth = HTTPBasicAuth(username, password), verify = False)
        return response_data.json()

    pool_data = makeRequest(username, password, BASE_URL + "/ltm/pool")

    for pools in pool_data['items']:
        #print pools['name']
        tildPath = pools['fullPath'].replace('/','~')

    #GET the Pool stats
        pool_stats = makeRequest(username, password, BASE_URL + "/ltm/pool/" + tildPath + "/stats")
        #print pool_stats['entries']['status.availabilityState']['description']

    #GET the Pool Members
        pool_members = makeRequest(username, password, BASE_URL + "/ltm/pool/" + tildPath + "/members")

        for members in pool_members['items']:
            for checkip in check_ip:
                if checkip ==  members['address']:
                    print pools['name'] + " " + pool_stats['entries']['status.availabilityState']['description'] + " " + members['name'] +" " + members['address'] + " " + members['state']

host_file.close()
check_ip.close()
