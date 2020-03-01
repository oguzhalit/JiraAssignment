import requests
import configparser
import json
import logging
import logging.config

logging.config.fileConfig(fname='log.conf')
logger = logging.getLogger('test')

config = configparser.ConfigParser()
config.read('auth.ini')

username = config['auth']['usern']
password = config['auth']['passw']
JiraUrl  = config['general']['jira_url']
BitbUrl  = config['general']['bitb_url']

def getJiraPages(URL):
    response = requests.get("%s/%s" % (JiraUrl,URL),
                            auth=(username, password))

    return response
def getBitbucPages(URL):
    response = requests.get("%s/%s" % (BitbUrl,URL),
                            auth=(username,password))
    return response

def createBitbucProject(projectName,projectKey):
    url = "%s/projects" % (BitbUrl)
    data = {
            "key": projectKey,
            "name": projectName
            }
    requests.post(url=url, json=data,auth=(username,password))
    logger.info("CreateBitbucketProject")

reproject = getJiraPages("project")

for project in reproject.json():
    projectName = project["name"]
    projectKey  = project["key"]
    logger.info("JiraProjectName: %s, JiraProjectKey: %s" % (projectName,projectKey))
    createBitbucProject(projectName,projectKey)


rebitbuct = getBitbucPages("projects")
for project in rebitbuct.json()['values']:
    projectName = project["name"]
    projectKey  = project["key"]
    logger.info("BitbucketProjectKey: %s BitbucketProjectName: %s" % (projectKey,projectName))

