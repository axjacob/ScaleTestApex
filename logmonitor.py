import requests,json, time
#import sqlite3
from sqlite3 import Error
from pygtail import Pygtail
import configparser 
min = 0
max = 10
def monitor():
        action = "/services/data/v50.0/sobjects/testept__e/"
        ept_json = queryDb()
        if ept_json != None:
                accesstoken, instanceUrl = login()
            
        if (accesstoken != None):
               for x in ept_json:
                       sendEvent(accesstoken,instanceUrl,action,json.dumps(x))
                       time.sleep(2)
                        
def login():
        cfg = configparser.ConfigParser()
        cfg.read("config.properties")
        gt = cfg.get('AUTH','grant_type')
        cid = cfg.get('AUTH','client_id')
        cs = cfg.get('AUTH','client_secret')
        email = cfg.get('AUTH','email')
        ptoken = cfg.get('AUTH','password')
        params = {
            "grant_type": gt,
            "client_id": cid, # Consumer Key
            "client_secret": cs, # Consumer Secret
            "username": email, # The email you use to login
            "password": ptoken # Concat your password and your security token
        }
        r = requests.post("https://test.salesforce.com/services/oauth2/token", params=params)
        print(r.content)
        # if you connect to a Sandbox, use test.salesforce.com instead
        access_token = r.json().get("access_token")
        instance_url = r.json().get("instance_url")
        authfile = open('authfile.txt','w+')
        authfile.write(access_token+","+instance_url)
        authfile.close()
        #print("Access Token:", access_token)
        #print("Instance URL", instance_url)
        return access_token, instance_url        
def sendEvent(jdata):
        access_token = None
        instance_url = None
        try:
                authfile = open('authfile.txt','r')
                logininfo = authfile.readline()
        except FileNotFoundError:
                access_token, instance_url = login()
        if logininfo:
                print("login file exists, reading info from there")
                access_token = logininfo.split(",")[0]
                instance_url = logininfo.split(",")[1]
                print(instance_url)
                authfile.close()
        else:
                access_token, instance_url = login()
        action = "/services/data/v50.0/sobjects/testept__e/"
        print(access_token, instance_url)
        headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
        }
        #jdata = json.loads(queryDb())
        jsondata = json.dumps(jdata)
        r = requests.request('POST', instance_url+action, headers=headers, data=jsondata, timeout=10)
        print('Debug: API %s call: %s' % ('POST', r.url) )
        if r.status_code > 300:
                raise Exception('API error when calling %s : %s' % (r.url, r.content))
        else:
                return r.json()
        
            
if __name__ == "__main__":
        login()