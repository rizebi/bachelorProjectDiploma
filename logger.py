import json
import os, sys
import logging
import datetime
import requests

##### Constants / Variables #####

#groups_file_path = "groups.json"
groups_file_path = "\\\\10.18.30.116\\atlassian_reports\\groups\\groups.json"
sonar_url = "https://sonar.bitdefender.biz/"
sonar_token = "2c04c4ad0002dbe9a0bebffcf8c530cf6842d5fb" #this is the token for admin2
#groups not to be synchronized:
ignored = ['bamboo-admin', 'bamboo-leads', 'confluence-administrators', 'confluence-extern', 'jira-administrators', 'jira-extern', 'stash-extern', 'stash-projectcreator']

##### Functions #####
def getLogger():
  now = datetime.datetime.now()
  log_name = "" + str(now.year) + "." + f"{now.month:02d}" + "." + f"{now.day:02d}" + "-sync_jira_sonar.log"
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log


# Returns a dictionary with key = name of group and values a list of members
# {"admins" : ["erizescu", "eene"], "users" : ["foo", "bar"]}
def getFileGroups():
  try:
    with open(groups_file_path) as f:
      groups = json.load(f)
    groups_dict = {}
    for group_json in groups:
      if group_json not in ignored:
        groups_dict[group_json] = groups[group_json]["members"]

    return groups_dict


  except Exception as e:
    log.info("Error: When reading the groups JSON: {}".format(e))
    sys.exit(1)

# Returns a dictionary with key = name of group and values a list of members
# {"admins" : ["erizescu", "eene"], "users" : ["foo", "bar"]}
def getSonarGroups():
  try:
    sonar_groups = requests.get(sonar_url + "api/user_groups/search", auth=(sonar_token, ''), params={'ps': 500}, verify=False)
    sonar_groups = sonar_groups.json()
    groups_dict = {}
    for group_json in sonar_groups["groups"]:
      group = group_json["name"]
      log.info("Sonar group: " + group)
      groups_dict[group] = []
      # now for current group we need to get it's users
      group_users = requests.get(sonar_url + "api/user_groups/users", params={'name': group, 'ps': 500}, auth=(sonar_token, ''), verify=False)
      group_users = group_users.json()

      group_users = group_users["users"]
      for user_json in group_users:
        user = user_json["login"]
        groups_dict[group].append(user)

    return groups_dict

  except Exception as e:
    log.info("Error: When getting Sonar groups: {}".format(e))
    sys.exit(2)


# Function that add the user received as parameter in the Sonar group received as parameter
def addUserSonar(user, group):
  try:
    response = requests.post(sonar_url + "api/user_groups/add_user", auth=(sonar_token, ''), params={'login': user, 'name': group}, verify=False)
    if response.status_code == 204:
      log.info("User " + user + " added.")
    if response.status_code == 404:
      log.info("Error: When adding user " + user + " in the Sonar group " + group + ": " + str(response.json()['errors'][0]['msg']))
      problems.write("User " + user + " does not exists (when trying to add in group " + group + ")\n")
  except Exception as e:
    log.info(("Error: When adding user " + user + " in the Sonar group " + group + ": {}").format(e))
    problems.write(("Error: When adding user " + user + " in the Sonar group " + group + ": {}\n").format(e))


# Function that creates the Sonar group received as parameter
# Returns true if successfully added, and folse otherwise
def createSonarGroup(group):
  try:
    requests.post(sonar_url + "api/user_groups/create", auth=(sonar_token, ''), params={'name': group}, verify=False)
    return True
  except Exception as e:
    log.info(("Error: When creating Sonar group " + group + ": {}").format(e))
    problems.write(("Error: When creating Sonar group " + group + ": {}\n").format(e))
    return False


##### BODY #####
log = getLogger()
try:
  log.info("\n")
  log.info("Starting syncing")

  log.info("Reading groups from file " + groups_file_path)
  file_groups = getFileGroups()
  log.info("File read. Found " + str(len(file_groups)) + " groups in the file")

  log.info("Getting existing groups from Sonar")
  sonar_groups = getSonarGroups()

  string_sonar_group = "{["
  for sonar_group in sonar_groups:
    string_sonar_group += '"' + sonar_group + '": ' + str(len(sonar_groups[sonar_group])) + ", "
  string_sonar_group = string_sonar_group[0:-2]
  string_sonar_group += "]}"
  log.info("We have found in Sonar " + str(len(sonar_groups)) + " groups:")
  log.info("Sonar groups are: " + string_sonar_group)


  problems = open("problems.txt", "a")


  for group in file_groups:
    log.info("**********************************Starting group: " + group)

    if group in sonar_groups.keys():
      # that means that the group already exists in Sonar, so we must update the users
      log.info("Group " + group + " already exists in Sonar")
      for file_user in file_groups[group]:
        if file_user in sonar_groups[group]:
          log.info("The user " + file_user + " is already in Sonar group " + group)
        else:
          log.info("The user " + file_user + " is not in Sonar group " + group + " so we must add it")
          addUserSonar(file_user, group)
    else:
      # that means that the group is not created in Sonar so first we must create it
      log.info("Creating Sonar group " + group)
      if createSonarGroup(group):
        log.info("Sonar group " + group + " created")
        for file_user in file_groups[group]:
          log.info("Adding user " + file_user + " in Sonar group " + group)
          addUserSonar(file_user, group)
      else:
        log.info("Cannot create Sonar group " + group)

  problems.close()


##### END #####
except KeyboardInterrupt:
    log.info("Quit")
    sys.exit(0)
except Exception as e:
    log.info("Fatal Error: {}".format(e))
    traceback.print_exc(file=sys.stdout)
    if len(errors_on_exit) > 0:
        log.info("I also found {} errors, while running".format(len(errors_on_exit)))
        for error in errors_on_exit:
            log.inf(eror)
    sys.exit(99)
