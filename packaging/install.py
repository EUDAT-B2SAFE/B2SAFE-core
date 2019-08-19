#!/usr/bin/env python
#
# epicclient.py
#
# * use 4 spaces!!! not tabs
# * set tabstop=4
# * set expandtab
# * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
# * use pylint
#

"""EUDAT configuration of iRODS B2SAFE and msiPID """

import getpass
import glob
import json
import os
import shutil
from datetime import datetime

CONFIG_FILE = 'install.json'
CONFIG_PARAMETERS = ["b2safe_package_dir",
                     "irods_conf_dir",
                     "irods_dir",
                     "irods_default_resource",
                     "cred_store_type",
                     "cred_file_path",
                     "server_id",
                     "server_api_reg",
                     "server_api_pub",
                     "handle_server_url",
                     "handle_private_key",
                     "handle_certificate_only",
                     "handle_prefix",
                     "handle_owner",
                     "handle_reverse_lookup_name",
                     "handle_reverse_lookup_password",
                     "handle_https_verify",
                     "handle_users",
                     "handle_groups",
                     "log_level",
                     "log_directory",
                     "shared_space",
                     "authz_enabled",
                     "msg_queue_enabled"]
PID_DEFAULT_PROFILE = [
    {
        "entry": {
            "index": 1,
            "type": "URL",
            "data": {
                "format": "string",
                "value": "{OBJECT}"
            }
        }
    },
    {
        "entry": {
            "index": 100,
            "type": "HS_ADMIN",
            "data": {
                "format": "admin",
                "value": {
                    "handle": "0.NA/{HANDLE_PREFIX}",
                    "index": 200,
                    "permissions": "011111110011"
                }
            }
        }
    }
]

########################
# Functions
########################


def add_irods_cmd_dir(json_config):
    '''
    add the iRODS path to the cmd directory.
    iRODS 4.2 and higher differs.
    4.1: /var/lib/irods/iRODS/server/bin/cmd
    4.2: /var/lib/irods/msiExecCmd_bin
    '''
    paths = [os.path.join(json_config["irods_dir"],
                          "iRODS",
                          "server",
                          "bin",
                          "cmd"),
             os.path.join(json_config["irods_dir"],
                          "msiExecCmd_bin")]
    for p in paths:
        if os.path.exists(p):
            json_config["irods_cmd_dir"] = p
            break

def check_user(json_config):
    ''' check the user who is running this program. It has to be the iRODS user '''

    username = getpass.getuser()
    service_account_config_file = json_config["irods_conf_dir"]+"/service_account.config"
    user_match = False

    try:
        with open(service_account_config_file) as service_account_config:
            for line in service_account_config:
                if line.rstrip() == 'IRODS_SERVICE_ACCOUNT_NAME='+username:
                    user_match = True
    except IOError:
        print "Error, Unable to open file: %s" % service_account_config_file
        exit(1)

    if user_match:
        print "The iRODS user matches the user who is running this script"
    else:
        print "The iRODS user  does not match the user who is running this script"
        exit(1)

def check_missing_parameters(json_config):
    ''' check the json config for missing keys '''

    parameters_match = True
    missing_parameters = []

    for parameter in CONFIG_PARAMETERS:
        if parameter not in json_config:
            parameters_match = False
            missing_parameters.append(parameter)

    if not parameters_match:
        print "Not all parameters are present. Please add following parameter(s)"
        for item in missing_parameters:
            print "The missing parameter = %s" % item
        exit(1)

def create_b2safe_symbolic_links(json_config):
    ''' create symbolic links for the b2safe rules, return files added to the config dict '''

    count = 0
    json_config["re_rulebase_set"] = []

    # delete existing symlinks
    for symlink_file in glob.glob(json_config["irods_conf_dir"]+'/eudat*.re'):
        try:
            os.unlink(symlink_file)
        except IOError:
            print "Error deleting symbolic link: %s" % symlink_file
            exit(1)

    # add new symlinks
    for symlink_file in glob.glob(json_config["b2safe_package_dir"]+'/rulebase/*.re'):
        try:
            os.symlink(symlink_file, json_config["irods_conf_dir"]+'/eudat'+str(count)+'.re')
            json_config["re_rulebase_set"].append('eudat'+str(count))
        except IOError:
            print "Error creating symbolic link: %s" % symlink_file
            exit(1)

        count = count + 1

def install_python_b2safe_scripts(json_config):
    ''' create symbolic links for python executables in b2safe package '''

    # add new symlinks
    for symlink_file in glob.glob(json_config["b2safe_package_dir"]+'/cmd/*.py'):
        destination_path = json_config["irods_cmd_dir"]+'/'+os.path.basename(symlink_file)
        try:
            # remove existing links
            if os.path.exists(destination_path):
                os.unlink(destination_path)
            # add new links
            os.symlink(symlink_file, destination_path)
        except IOError:
            print "Error creating symbolic link: %s" % symlink_file
            exit(1)
        except OSError:
            print "Error creating symbolic link: " + symlink_file + ", " + destination_path
            exit(1)

def read_json_config(json_config_file):
    ''' read the parameters from a json config file '''

    try:
        with open(json_config_file) as config_file:
            json_config = json.load(config_file)
    except IOError:
        print "Error, Unable to open file: %s" % json_config_file
        exit(1)

    return dict(json_config)

def secure_file(chmod_file):
    ''' set the protection to rw for the owner only '''

    if os.path.exists(chmod_file):
        try:
            os.chmod(chmod_file, 0o600)
        except IOError:
            print "Error, Unable to protect file: %s" % chmod_file
            exit(1)
    else:
        print "Error, Unable to protect file: %s as it not present" % chmod_file
        exit(1)

def save_config_file(save_file):
    ''' make first copy of the day of config file '''

    save_file_copy = save_file+'.org.'+datetime.now().strftime('%Y%m%d')

    # check if file exists and if not copy
    if not os.path.exists(save_file_copy):
        try:
            shutil.copy2(save_file, save_file_copy)
            secure_file(save_file_copy)
        except IOError:
            print "Error, Unable to copy file: %s" % save_file
            exit(1)

def update_authz_map(json_config):
    ''' update the authz map json file '''

    authz_map_file = json_config["b2safe_package_dir"]+'/conf/authz.map.json'

    # save authz file
    save_config_file(authz_map_file)

    # read authz file
    authz_map_config = read_json_config(authz_map_file)

    print "TODO: Update %s not yet implemented !! " % authz_map_file

    ### write authz config
    ##write_json_config(authz_map_config, authz_map_file)

def update_epicclient_credentials(json_config):
    ''' create (if needed) and update epicclient2.py credentials file '''

    credentials_file = json_config["cred_file_path"]

    # create credentials file
    if not os.path.exists(credentials_file):
        shutil.copy2(json_config["b2safe_package_dir"]+'/conf/credentials_epicclient2_example',
                     credentials_file)
        secure_file(credentials_file)

    # save credentails file
    save_config_file(credentials_file)

    # read credentials file
    epicclient2_config = read_json_config(credentials_file)

    # modify epicclient2 credentials
    epicclient2_config["handle_server_url"] = json_config["handle_server_url"]
    epicclient2_config["private_key"] = json_config["handle_private_key"]
    epicclient2_config["certificate_only"] = json_config["handle_certificate_only"]
    epicclient2_config["prefix"] = json_config["handle_prefix"]
    epicclient2_config["handleowner"] = json_config["handle_owner"]
    epicclient2_config["reverselookup_username"] = json_config["handle_reverse_lookup_name"]
    epicclient2_config["reverselookup_password"] = json_config["handle_reverse_lookup_password"]
    epicclient2_config["HTTPS_verify"] = json_config["handle_https_verify"]

    # write credentials config
    write_json_config(epicclient2_config, credentials_file)

def update_flat_file_parameter(modify_file, mod_key, mod_value, irods_file=False):
    ''' update a file and make it 'key = "value";' '''

    lines = []
    key_match = False

    try:
        # read file in list
        with open(modify_file) as file_handle:
            for line in file_handle:
                line = line.rstrip()
                lines.append(line)
    except IOError:
        print "Error, Unable to open file: %s" % modify_file
        exit(1)

    for idx, line in enumerate(lines):
        stripped_line = line.lstrip()
        if stripped_line.find(mod_key, 0, len(mod_key)) == 0:
            key_match = True
            if irods_file:
                start_s = line.find('"')
                end_s = line.find('"', start_s+1)
                newline = line[0:start_s+1]+str(mod_value)+line[end_s:len(line)]
                lines[idx] = newline

    if key_match:
        try:
            with open(modify_file, "w+") as config_file:
                config_file.write("\n".join(lines))
        except IOError:
            print "Error, Unable to open file: %s" % modify_file
            exit(1)
    else:
        print "Parameter %s not found in file %s !!!" % (mod_key, modify_file)

def update_irods_server_config(json_config):
    ''' add the eudat rules to the iRODS server config '''

    config_file = json_config["irods_conf_dir"]+'/server_config.json'

    # save iRODS config file
    save_config_file(config_file)

    # read iRODS config
    irods_config = read_json_config(config_file)

    # modify iRODS config
    for item in json_config["re_rulebase_set"]:
        match_item = False
        match_dict = False
        # In 4.2.1 and higher it is an single item under plugin_configuration.
        # in version 4.1.x it is a dict under 're_rulebase_set'.
        if not "re_rulebase_set" in irods_config.keys():
            for irods_rule_engine in irods_config["plugin_configuration"]["rule_engines"]:
                if irods_rule_engine["plugin_name"] == "irods_rule_engine_plugin-irods_rule_language":
                    for irods_config_item in irods_rule_engine["plugin_specific_configuration"]["re_rulebase_set"]:
                        if item == irods_config_item:
                            match_item = True
        else:
            match_dict = True
            for irods_config_item in irods_config["re_rulebase_set"]:
                if item == irods_config_item["filename"]:
                    match_item = True
        # append to the list/array only if needed. Either dict or single item.
        if not match_item and not match_dict:
            for irods_rule_engine in irods_config["plugin_configuration"]["rule_engines"]:
                if irods_rule_engine["plugin_name"] == "irods_rule_engine_plugin-irods_rule_language":
                    irods_rule_engine["plugin_specific_configuration"]["re_rulebase_set"].append(item)
        elif not match_item and match_dict:
            append_item_dict = {'filename': item}
            irods_config["re_rulebase_set"].append(append_item_dict)

    # write iRODS config
    write_json_config(irods_config, config_file)

def update_local_re_parameters(json_config):
    ''' update parameters in local.re B2SAFE ruleset '''

    config_file = json_config["b2safe_package_dir"]+'/rulebase/local.re'

    # save B2SAFE rule file
    save_config_file(config_file)

    # update B2SAFE rule file

    # getAuthZParameters
    update_flat_file_parameter(config_file, '*authZMapPath',
                               json_config["b2safe_package_dir"]+'/conf/authz.map.json', True)

    # getConfParameters
    update_flat_file_parameter(config_file, '*authzEnabled',
                               str(json_config["authz_enabled"]).lower(), True)
    update_flat_file_parameter(config_file, '*messageQueueEnabled',
                               str(json_config["msg_queue_enabled"]).lower(), True)

    # getEpicApiParameters
    update_flat_file_parameter(config_file, '*credStoreType', json_config["cred_store_type"], True)
    update_flat_file_parameter(config_file, '*credStorePath', json_config["cred_file_path"], True)
    update_flat_file_parameter(config_file, '*serverID', json_config["server_id"], True)

    # getHttpApiParameters
    update_flat_file_parameter(config_file, '*serverApireg', json_config["server_api_reg"], True)
    update_flat_file_parameter(config_file, '*serverApipub', json_config["server_api_pub"], True)

    # getMetaParameters
    update_flat_file_parameter(config_file, '*metaConfPath',
                               json_config["b2safe_package_dir"]+'/conf/metadataManager.conf', True)

    # getLogParameters
    update_flat_file_parameter(config_file, '*logConfPath',
                               json_config["b2safe_package_dir"]+'/conf/log.manager.json', True)

def update_log_manager_conf(json_config):
    ''' update log manager config file '''

    log_manager_conf_file = json_config["b2safe_package_dir"]+'/conf/log.manager.json'
    logmanager_config = {}

    # save logmanager file
    if os.path.exists(log_manager_conf_file):
        save_config_file(log_manager_conf_file)

    # read logmanager config
    if os.path.exists(log_manager_conf_file):
        logmanager_config = read_json_config(log_manager_conf_file)

    # modify logmanager config
    logmanager_config["log_level"] = json_config["log_level"]
    logmanager_config["log_dir"] = json_config["log_directory"]

    # write logmanager config
    write_json_config(logmanager_config, log_manager_conf_file)

def update_pid_uservice_config(json_config):
    ''' update pid uService json file '''

    pid_uservice_conf_file = json_config["irods_conf_dir"]+'/irods_pid.json'
    handle_url_without_port = json_config["handle_server_url"].split(":")[0] + ":" \
                              + json_config["handle_server_url"].split(":")[1]
    handle_url_port = json_config["handle_server_url"].split(":")[2]

    irods_server = str(json_config["server_id"].split(":")[1])[2:]
    irods_url_port = json_config["server_id"].split(":")[2]

    webdav_server = str(json_config["server_api_pub"].split(":")[0]) + ":" \
                             + json_config["server_api_pub"].split(":")[1]
    webdav_url_port = "80"
    if len(json_config["server_api_pub"].split(":")) > 2:
        webdav_url_port = json_config["server_api_pub"].split(":")[2]

    if json_config["handle_https_verify"].lower() == 'true':
        handle_lookup_insecure = False
        handle_lookup_cacert = None
    elif json_config["handle_https_verify"].lower() == 'false':
        handle_lookup_insecure = True
        handle_lookup_cacert = None
    else:
        handle_lookup_insecure = False
        handle_lookup_cacert = json_config["handle_https_verify"]

    # create pid uService file
    if not os.path.exists(pid_uservice_conf_file):
        shutil.copy2(pid_uservice_conf_file+'.02_custom_profile',
                     pid_uservice_conf_file)
        secure_file(pid_uservice_conf_file)

    # save pid uService file
    save_config_file(pid_uservice_conf_file)

    # read pid uService config
    pid_uservice_config = read_json_config(pid_uservice_conf_file)

    # handle service
    pid_uservice_config["handle"]["url"] = handle_url_without_port+'/api/handles'
    pid_uservice_config["handle"]["port"] = int(handle_url_port)
    pid_uservice_config["handle"]["prefix"] = json_config["handle_prefix"]
    pid_uservice_config["handle"]["cert"] = json_config["handle_certificate_only"]
    pid_uservice_config["handle"]["key"] = json_config["handle_private_key"]
    pid_uservice_config["handle"]["insecure"] = handle_lookup_insecure
    pid_uservice_config["handle"]["cacert"] = handle_lookup_cacert
    pid_uservice_config["handle"]["profile"] = PID_DEFAULT_PROFILE

    # irods
    pid_uservice_config["irods"]["server"] = irods_server
    pid_uservice_config["irods"]["port"] = int(irods_url_port)
    pid_uservice_config["irods"]["url_prefix"] = json_config["server_id"]
    pid_uservice_config["irods"]["webdav_prefix"] = webdav_server
    pid_uservice_config["irods"]["webdav_port"] = int(webdav_url_port)

    # reverse lookup
    pid_uservice_config["lookup"]["url"] = handle_url_without_port+'/hrls/handles'
    pid_uservice_config["lookup"]["port"] = int(handle_url_port)
    pid_uservice_config["lookup"]["prefix"] = json_config["handle_prefix"]
    pid_uservice_config["lookup"]["user"] = json_config["handle_reverse_lookup_name"]
    pid_uservice_config["lookup"]["password"] = json_config["handle_reverse_lookup_password"]
    pid_uservice_config["lookup"]["insecure"] = handle_lookup_insecure
    pid_uservice_config["lookup"]["cacert"] = handle_lookup_cacert
    pid_uservice_config["lookup"]["before_create"] = False

    # permissions
    if 'handle_users' in json_config:
        pid_uservice_config["permissions"]["users_create"] = json_config["handle_users"]
        pid_uservice_config["permissions"]["users_delete"] = json_config["handle_users"]
        pid_uservice_config["permissions"]["users_write"] = json_config["handle_users"]
    if 'handle_groups' in json_config:
        pid_uservice_config["permissions"]["groups_create"] = json_config["handle_groups"]
        pid_uservice_config["permissions"]["groups_delete"] = json_config["handle_groups"]
        pid_uservice_config["permissions"]["groups_write"] = json_config["handle_groups"]

    # print json.dumps(pid_uservice_config, indent=2, sort_keys=True)
    # write pid uService config
    write_json_config(pid_uservice_config, pid_uservice_conf_file)



def write_json_config(json_dict, json_config_file):
    ''' write the parameters from a dict to a json config file '''

    try:
        with open(json_config_file, "w+") as config_file:
            config_file.write(json.dumps(json_dict, indent=4, sort_keys=True))
    except IOError:
        print "Error, Unable to open file: %s" % json_config_file
        exit(1)


########################
# main program
########################

#
# read parameter file
#
B2SAFE_CONFIG = read_json_config(CONFIG_FILE)

#
# check user doing actions. It should be the user from:
# /etc/irods/service_account.config
#
check_user(B2SAFE_CONFIG)

#
# check for missing parameters in config
#
check_missing_parameters(B2SAFE_CONFIG)

#
# We only support iRODS 4.1 and higher
# add cmd directory to B2SAFE_CONFIG
#
add_irods_cmd_dir(B2SAFE_CONFIG)

#
# create symbolic links to the eudat rulebase
#
create_b2safe_symbolic_links(B2SAFE_CONFIG)

#
# edit /etc/irods/server_config.json
# append eudat specific rules to to reRuleSet.
# we use links in the type of eudatxy.re.
# (make sure to include the comma and no spaces)
#
update_irods_server_config(B2SAFE_CONFIG)

#
# install python scripts
#
install_python_b2safe_scripts(B2SAFE_CONFIG)

#
# properly configure the default resource in /etc/irods/core.re
#
## NOT DONE !!! We do not kill the users config.
#

#
# Set the proper values in the epicclient2.py  credentials file
#
update_epicclient_credentials(B2SAFE_CONFIG)

#
# Set the pid uService parameters
#
update_pid_uservice_config(B2SAFE_CONFIG)

#
# update the 'getAuthZParameters'   rule in '/opt/eudat/b2safe/rulebase/local.re'
# update the "getConfParameters"    rule in "/opt/eudat/b2safe/rulebase/local.re"
# update the 'getEpicApiParameters' rule in '/opt/eudat/b2safe/rulebase/local.re'
# update the "getHttpApiParameters" rule in "/opt/eudat/b2safe/rulebase/local.re"
# update the "getMetaParameters"    rule in "/opt/eudat/b2safe/rulebase/local.re"
# update the "getLogParameters"     rule in "/opt/eudat/b2safe/rulebase/local.re"
#
update_local_re_parameters(B2SAFE_CONFIG)

#
# update authz.map.json
#
update_authz_map(B2SAFE_CONFIG)

#
# update log.manager.conf
#
update_log_manager_conf(B2SAFE_CONFIG)
