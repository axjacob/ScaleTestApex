import requests
import configparser

def getMachineId():
    url = "http://169.254.169.254/latest/meta-data/instance-id"
    r = requests.get(url,timeout=5)
    return r.content

def updateEnv():
    Id = getMachineId()
    print(Id)
    config = configparser.ConfigParser()
    config.read('testrunner.properties')
    config['environment']['machine.Id']=str(Id)
    with open('testrunner.properties', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    updateEnv()