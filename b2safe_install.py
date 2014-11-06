#!/usr/bin/python
""" B2SAFE automatic deployment """
import os
import getpass
import commands
import subprocess
import glob

# colors for terminal output

RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
BACK = '\033[0m'
BOLD = '\033[1m'

# read and set config values

filename = "./b2safe.config"
try:
    fr = open(filename,'r')
except IOError:
    print RED + BOLD + 'Error: cannot open file' + filename + '\n' \
          'Please, check if the source download was '\
          'complete and start over again.' + BACK
    exit()

lines = fr.readlines()
for line in lines:
    if line.find('IRODS_DIR') > -1:
        ird = line.split()
    if line.find('SOURCE_DIR') > -1:
        tr = line.split()
    if line.find('B2SAFE_MODULE_DIR:') > -1:
        bmd = line.split()
    if line.find('DEFAULT_RESOURCE') > -1:
        dr = line.split()
    if line.find('CRED_STORE_TYPE') > -1:
        cst = line.split()
    if line.find('CRED_FILE_PATH') > -1:
        cfp = line.split()
    if line.find('SERVER_ID') > -1:
        si = line.split()
    if line.find('BASE_URI') > -1:
        bu = line.split()
    if line.find('USERNAME') > -1:
        un = line.split()
    if line.find('PREFIX') > -1:
        pf = line.split()
    if line.find('USERS') > -1:
        us = line.split()
    if line.find('LOG_LEVEL') > -1:
        ll = line.split()
    if line.find('LOG_DIR') > -1:
        ld = line.split()
    if line.find('SHARED_SPACE') > -1:
        hs = line.split()
fr.close()    

IRODS_DIR = ird[1]
SOURCE_DIR = tr[1]
B2_MOD_DIR = bmd[1]
DEFAULT_RESOURCE = dr[1]
CRED_STORE_TYPE = cst[1]
CRED_FILE_PATH = cfp[1]
SERVER_ID = si[1]
BASEURI = bu[1]
USERNAME = un[1]
PREFIX = pf[1]
LOG_LEVEL = ll[1]
LOG_DIR = ld[1]
SHARED_SPACE = hs[1]

def inpt(inp1):
    """ y/n exit """
    for j in range(3):
        if inp1 == 'y':
            break
        if inp1 == 'n':
            print BLUE + BOLD + 'Exiting.. Installation was not complete. ' \
                  + BACK
            exit()
        else:
            inp1 = raw_input(RED + 'Please, respond in (y/n) :' + BACK).lower()
    if inp1 == 'y':
        return True
    else:
        print RED + BOLD + 'Exiting.. Installation was not complete. ' + BACK
        exit()
    return False

def symlink(orign, link, oldlink1, oldlink2):
    """ create symbolic links """
    subprocess.call(["rm", "-f", oldlink1])
    subprocess.call(["rm", "-f", oldlink2])
    try:
        subprocess.check_call(["stat", orign])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: file ' + orign \
        + ' does not exist. \nPlease, check if the source download was ' \
        'complete and start over again.' + BACK
        exit()
    else:
        try:
            subprocess.check_call(["ln", "-s", orign, link])
        except subprocess.CalledProcessError:
            print RED + BOLD + 'Error: failed to create symbolic link:\n' + \
              link + '\nPlease, check command line output and start over '\
              'again.' + BACK
            exit()

def stat(obj):
    """ stat object """
    try:
        subprocess.check_call(["stat", obj])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: file/directory ' + obj + \
              ' does not exist.\nPlease, check:\n' \
              '1) if the source download was complete;\n' \
              '2) if the path in the b2safe.config is correct;\n' \
              '3) your iRODS installation and start over again.' + BACK
        exit()

def check(strr, fname):
    """ check if string is in file """
    datafile = file(fname) 
    for lin in datafile:
        if strr in lin: 
            return True
    return False

# welcome msgs

print GREEN + BOLD + 'Welcome! \n This script will install EUDAT B2SAFE ' \
      'module in the following directory: ' + B2_MOD_DIR + BACK
print BLUE + BOLD + 'CAUTION: ' \
      'If there is a previuos version of the B2SAFE module installed ' \
      'in this directory, it will be overwritten. \n' + BACK

inp = raw_input(BLUE + BOLD + 'Continue installation (y/n)? :' + BACK).lower()

chk = inpt(inp)

print BLUE + BOLD + 'CAUTION: ' \
            'If you were using a previuos version of the B2SAFE module, \n' \
            '1) your ' + IRODS_DIR + '/server/config/reConfigs/ ' \
            'may contain symbolic ' \
            'links to B2SAFE scripts of the previous version. '\
            'They may have (but not must and are not limited to) ' \
            'names like: \n' \
            + IRODS_DIR + '/server/config/reConfigs/eudat.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eudat-v1.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eurepl.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/catchError.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eucerr.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eudat-authZ-filters.re\n' \
            + IRODS_DIR + '/server/config/reConfigs/local.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/euloc.re \n' \
            '2)your ' + IRODS_DIR + '/server/bin/cmd/ may contain' \
            ' symbolic links to ' \
            'B2SAFE scripts of the previous version. They may have (but not ' \
            'must and are not limited to) names like: \n' \
            + IRODS_DIR + '/server/bin/cmd/authZ.manager.py \n' \
            + IRODS_DIR + '/server/bin/cmd/authz.map.json \n' \
            + IRODS_DIR + '/server/bin/cmd/credentials_example \n' \
            + IRODS_DIR + '/server/bin/cmd/credentials \n' \
            + IRODS_DIR + '/server/bin/cmd/epicclient.py \n' \
            + IRODS_DIR + '/server/bin/cmd/epicclient21.py \n' \
            + IRODS_DIR + '/server/bin/cmd/log.manager.conf \n' \
            + IRODS_DIR + '/server/bin/cmd/log.manager.py \n' \
            + IRODS_DIR + '/server/bin/cmd/statpid.py \n' \
            'Please, check and remove these old symbolic links. ' \
            'Otherwise, the new module will not work correctly. ' \
            'If you were not using the previous version ' \
            'of the B2SAFE module and there are no such '\
            'symbolic links in your irods directories, you can ' \
            'proceed with this installation. Otherwise, plese, quit it, ' \
            'remove mentioned above symbolic links and start ' \
            'the installation again. \n' + BACK

inp = raw_input(BLUE + BOLD + 'Continue installation (y/n)? :' + BACK).lower()

chk = inpt(inp)

print 'copy source_dir to modules dir in irods'

try:
    subprocess.check_call(["stat", B2_MOD_DIR])
except subprocess.CalledProcessError:
    print BLUE + BOLD + 'Creating directory ' + B2_MOD_DIR + '..' + BACK
    try:
        subprocess.check_call(["mkdir", B2_MOD_DIR])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: directory ' + B2_MOD_DIR + ' cannot be ' \
          'created. \nPlease, check the path in the b2safe.config ' \
          '(B2SAFE_MODULE_DIR) \nand access permissions and start over again.' \
          + BACK
        exit()
    else:
        subprocess.call(["mkdir", B2_MOD_DIR])
else:
    print RED + BOLD + 'Directory ' + B2_MOD_DIR + ' exists. \n' + BACK
    inp = raw_input(RED + BOLD + 'Should it be overwritten (y/n)? :' \
          + BACK).lower()
    chk = inpt(inp)

stat(SOURCE_DIR)

try:
    subprocess.call(["cp", "-r"] + glob.glob(os.path.join(SOURCE_DIR, '*')) \
                    + [B2_MOD_DIR])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: cannot copy ' + SOURCE_DIR + ' to ' \
          + B2_MOD_DIR + '\nPlease, check access permissions and start over' \
          ' again.' + BACK
    exit()

try:
    subprocess.check_call(["stat", B2_MOD_DIR + "/microservices/obj"])
except subprocess.CalledProcessError:
    try:
        subprocess.check_call(["mkdir", B2_MOD_DIR + "/microservices/obj"])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: directory ' + B2_MOD_DIR + \
              '/microservices/obj' + ' cannot be created. \n' \
              'Please, check the path in the b2safe.config ' \
              '(B2SAFE_MODULE_DIR) \nand access permissions and start ' \
              'over again.' + BACK
        exit()
    else:
        subprocess.call(["mkdir", B2_MOD_DIR + "/microservices/obj"])

filename =  B2_MOD_DIR + "/Makefile"

try:
    os.rename(filename, filename+"~")
except OSError:
    print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
    'Please, check if the source download was complete and start over ' \
    'again.' + BACK
    exit()

destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('/lat/irods') > -1:
        line1 = line.replace("/lat/irods", IRODS_DIR)
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print '1.1. <irods>/scripts/configure --enable-B2SAFE \n'\
'If a previous version of the module is present, \n'\
'disable it before to install the new one \n'\
'(if the directory name is the same, change it): \n'\
'<irods>/scripts/configure --disable-OLD_MODULE --enable-B2SAFE'

try:
    os.chdir(IRODS_DIR)
except OSError:
    print RED + BOLD + 'Error: directory ' + IRODS_DIR + 'does not exist.\n' \
              'Please, check the path in the b2safe.config (IRODS_DIR) \n' \
              'and access permissions and start over again.' + BACK
    exit()

stat(IRODS_DIR + "/scripts/configure")

try:
    subprocess.call([IRODS_DIR + "/scripts/configure", "--enable-B2SAFE"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: Cannot execute ' + IRODS_DIR + \
          '/scripts/configure. \nPlease, check your access permissions and ' \
          'start over again.' + BACK
    exit()

print '1.2. make clean'

try:
    subprocess.check_call(["make", "clean"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: Cannot execute make.\nPlease, check your ' \
          'iRODS Makefile and start over again.' + BACK
    exit()

print '1.3. make'

try:
    subprocess.check_call(["make"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: iRODS compilation was not successful.\n' \
          'Please, check your command line output and start over again' + BACK
    exit()

print '1.4 <irods>/irodsctl restart'

try:
    subprocess.check_call([IRODS_DIR + "/irodsctl", "restart"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: iRODS compilation was not successful.\n' \
          'Please, check your command line output and start over again' + BACK
    exit()

print '2. create symbolic links to the eudat rulebase'

symlink(B2_MOD_DIR + "/rulebase/eudat.re", \
        IRODS_DIR + "/server/config/reConfigs/eudat.re", \
        IRODS_DIR + "/server/config/reConfigs/eudat.re", \
        IRODS_DIR + "/server/config/reConfigs/eudat-v1.re")

symlink(B2_MOD_DIR + "/rulebase/replication.re", \
        IRODS_DIR + "/server/config/reConfigs/eurepl.re", \
        IRODS_DIR + "/server/config/reConfigs/replication.re", \
        IRODS_DIR + "/server/config/reConfigs/eurepl.re")

symlink(B2_MOD_DIR + "/rulebase/pid-service.re", \
        IRODS_DIR + "/server/config/reConfigs/eupids.re", \
        IRODS_DIR + "/server/config/reConfigs/pid-service.ree", \
        IRODS_DIR + "/server/config/reConfigs/eupids.re")

symlink(B2_MOD_DIR + "/rulebase/catchError.re", \
        IRODS_DIR + "/server/config/reConfigs/eucerr.re", \
        IRODS_DIR + "/server/config/reConfigs/catchError.re", \
        IRODS_DIR + "/server/config/reConfigs/eucerr.re")

symlink(B2_MOD_DIR + "/rulebase/local.re", \
        IRODS_DIR + "/server/config/reConfigs/euloc.re", \
        IRODS_DIR + "/server/config/reConfigs/local.re", \
        IRODS_DIR + "/server/config/reConfigs/euloc.re")

print '3. edit <irods>/server/config/server.config and append '\
',eudat,eurepl,eupids,eucerr,euloc'\
',to reRuleSet (make sure to include the comma and no spaces)'

filename = IRODS_DIR + "/server/config/server.config"
try:
    os.rename(filename, filename+"~")
except OSError:
    print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
    'Please, check your iRODS installation and start over again.' + BACK
    exit()
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('reRuleSet') > -1:
        if (line.find('eudat') < 0) and \
(line.find('replication') < 0):
            destination.write(line.strip("\n") + \
",eudat,eurepl,eupids,eucerr,euloc" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') < 0) and (line.find('eurepl') < 0):
            destination.write(line.strip("\n") + \
",eurepl,eupids,eucerr,euloc" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') > -1):
            line1 = line.replace("replication","eurepl")
            line1 = line1.replace("pid-service","eupids")
            line1 = line1.replace("catchError","eucerr")
            line1 = line1.replace("local","euloc")
            destination.write(line1)
        else:
            destination.write(line)
    else:
        destination.write(line)
source.close()
destination.close()

print "4. configure iRODS hooks. \n"\
"    edit the <irods>/server/config/reConfigs/core.re file "\
"and add the following two acPostProcForPutHooks: \n"\
"    acPostProcForPut { \n        ON($objPath like "\
"'\*.replicate') { \n            "\
"processReplicationCommandFile($objPath);}} \n    "\
"acPostProcForPut { \n        "\
"ON($objPath like '\*.pid.create') { \n"\
"            processPIDCommandFile($objPath);}} "

filename = IRODS_DIR + "/server/config/reConfigs/core.re"
stat(filename)
if not check("\*.pid.create", filename):
    try:
        os.rename(filename, filename+"~")
    except OSError:
        print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
              'Please, check your iRODS installation and start over again.' \
              + BACK
        exit()
    destination = open(filename, "w")
    source = open(filename+"~", "r")
    for line in source:
        if line.find('# 4) acPostProcForPut') > -1:
            destination.write(line)
            destination.write('acPostProcForPut {' + '\n')
            destination.write(\
'    ON($objPath like "\*.replicate") {' + '\n')
            destination.write(\
'        processReplicationCommandFile($objPath);}}' + '\n')
            destination.write('acPostProcForPut {' + '\n')
            destination.write(\
'    ON($objPath like "\*.pid.create") {' + '\n')
            destination.write(\
'        processPIDCommandFile($objPath);}}' + '\n')
        else:
            destination.write(line)
    source.close()
    destination.close()

print '5. properly configure the default resource in '\
'<irods>/server/config/reConfigs/core.re \n'

if not check('acSetRescSchemeForCreate {msiSetDefaultResc("'\
 + DEFAULT_RESOURCE + '","null"); }',filename) \
and DEFAULT_RESOURCE != 'demoResc':
    try:
        os.rename(filename, filename+"~")
    except OSError:
        print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
              'Please, check your iRODS installation and start over again.' \
              + BACK
        exit()
    destination = open(filename, "w")
    source = open(filename+"~", "r")
    for line in source:
        if line.find('acSetRescSchemeForCreate {msiSetDefaultResc') > -1:
            destination.write('#'+line)
        elif line.find('acSetRescSchemeForRepl {msiSetDefaultResc') > -1:
            destination.write('#'+line)
        elif line.find('also apply to acSetRescSchemeForRepl') > -1:
            destination.write(line)
            destination.write('acSetRescSchemeForCreate '\
'{msiSetDefaultResc("' + DEFAULT_RESOURCE + '","null"); }' + '\n')
            destination.write('acSetRescSchemeForRepl '\
'{msiSetDefaultResc("' + DEFAULT_RESOURCE + '","null"); }' + '\n')
        else:
            destination.write(line)
    source.close()
    destination.close()

print '6.1 install python scripts \n     cd <irods> \n     '\
'ln -s <absolute-irods-path>/modules/B2SAFE/cmd/* '\
'./server/bin/cmd/ \n     check permissions on the scripts '\
'and make sure they are executable by the irods user \n'\
'         e.g.chmod u+x cmd/* \n'

stat(B2_MOD_DIR + "/cmd")

subprocess.call(["chmod", "u+x"] + \
                 glob.glob(os.path.join(B2_MOD_DIR, 'cmd', '*')))

subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authZ.manager.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authz.map.json"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authz.map.json~"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/credentials_example"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/credentials"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/epicclient.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/epicclient21.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/log.manager.conf"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/log.manager.conf~"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/log.manager.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/statpid.py"])

try:
    subprocess.check_call(["ln", "-s"] + \
    glob.glob(os.path.join(B2_MOD_DIR, 'cmd', '*')) + \
    [IRODS_DIR + "/server/bin/cmd/"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: failed to create symbolic link:\n' + \
          IRODS_DIR + '/server/bin/cmd/*\nPlease, check command line output' \
          'and start over again.' + BACK
    exit()

try:
    subprocess.check_call(["ln", "-s"] + \
    glob.glob(os.path.join(B2_MOD_DIR, 'conf', '*')) + \
    [IRODS_DIR + "/server/bin/cmd/"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: failed to create symbolic link:\n' + \
          IRODS_DIR + '/server/bin/cmd/*\nPlease, check command line output' \
          'and start over again.' + BACK
    exit()

print "6.2 update the 'getEpicApiParameters' rule in "\
"'./server/config/reConfigs/euloc.re' \n     "\
"- Configure the credential storage type: 'os': "\
"stored on the local filesystem or 'irods': stored on de irods namespace. "\
"\n     - Set the path to the credentials file \n"\
"     - set the correct serverID to include the fully qualified hostname. "\
"For instance: 'irods://node.domain.com:1247' \n     "\
"- Set the proper values in the credentials file "\
"(see ./conf/credentials_example for an example) "

filename = B2_MOD_DIR + "/rulebase/local.re"
try:
    os.rename(filename, filename+"~")
except OSError:
    print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
          'Please, check your iRODS installation and start over again.' \
          + BACK
    exit()
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('"os"') > -1:
        line1 = line.replace("os", CRED_STORE_TYPE)
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/credentials_test"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/credentials_test",CRED_FILE_PATH)
        destination.write(line1)
    elif line.find('"irods://<hostnameWithFullDomain>:1247"') > -1:
        line1 = line.replace("irods://<hostnameWithFullDomain>:1247", SERVER_ID)
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/authz.map.json"') > -1:
        line1 = line.replace("/srv/irods/current/modules/B2SAFE/"\
"cmd/authz.map.json",B2_MOD_DIR+"/conf/authz.map.json")
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf",\
B2_MOD_DIR+"/conf/log.manager.conf")
        destination.write(line1) 	
    else:
        destination.write(line)
source.close()
destination.close()

print "- Set the proper values in the credentials "\
"file (see ./conf/credentials_example for an example)"

filename = B2_MOD_DIR + "/conf/credentials_example"
stat(filename)
destination = open(B2_MOD_DIR+"/conf/credentials","w")
source = open(filename, "r")
for line in source:
    if line.find('"baseuri"') > -1:
        line1 = line.replace("https://epic.sara.nl/v2_test/handles/", BASEURI)
        destination.write(line1)
    elif line.find('"username"') > -1:
        line1 = line.replace("XXX", USERNAME)
        destination.write(line1)
    elif line.find('"prefix"') > -1:
        line1 = line.replace("ZZZ", PREFIX)
        destination.write(line1)
    elif line.find('"password"') > -1:
        print BLUE + BOLD + "Please, enter your password for your prefix " \
              + PREFIX + ":" + BACK
        password = getpass.getpass()
        line1 = line.replace("YYYYYYYY", password)
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print '6.3 update the "getAuthZParameters" rule in '\
'"./server/config/reConfigs/euloc.re" \n - '\
'Set the proper values in modules/B2SAFE/conf/authz.map.json'

filename = B2_MOD_DIR + "/conf/authz.map.json"
try:
    os.rename(filename, filename+"~")
except OSError:
    print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
          'Please, check your iRODS installation and start over again.' \
          + BACK
    exit()
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('"subject"') > -1:
        destination.write(line)
        destination.write('                [')
        for i in range(1, len(us)-1):
            print us[i]
            destination.write(' "'+us[i]+'",')
        destination.write(' "'+us[len(us)-1]+'" ],' + '\n')
    elif line.find('"action"') > -1:
        destination.write(line)
        destination.write('                [ "read" ],' + '\n')
    elif line.find('"target"') > -1:
        destination.write(line)
        destination.write('                [ "'+ B2_MOD_DIR +'/cmd/*" ' + ',')
        destination.write(' "'+B2_MOD_DIR+'/conf/*" ]' + '\n')
    elif line.find('"*"') < 0:
        destination.write(line)
source.close()
destination.close()

print '6.4 update the "getLogParameters" rule in '\
'"./server/config/reConfigs/euloc.re" \n '\
'- Set the proper values in modules/B2SAFE/conf/log.manager.conf'

filename = B2_MOD_DIR + "/conf/log.manager.conf"
try:
    os.rename(filename, filename+"~")
except OSError:
    print RED + BOLD + 'Error: file ' + filename + ' does not exist. ' \
          'Please, check your iRODS installation and start over again.' \
          + BACK
    exit()
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('"log_level"') > -1:
        line1 = line.replace("DEBUG", LOG_LEVEL)
        destination.write(line1)
    elif line.find('"log_dir"') > -1:
        line1 = line.replace("/srv/irods/current/modules/B2SAFE/log", LOG_DIR)
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print '7. create a shared space in all zones as configured in the '\
'eudat.re rulebase getSharedCollection function. \n - defaults to '\
'"<zone>/replicate" \n - make sure all users involved in the '\
'replication can write in this collection.'

path = os.environ["PATH"]
if path.find('icommands') < 0:
    path = path + ":" + IRODS_DIR + "/clients/icommands/bin"
    os.putenv('PATH', path)
    os.system('bash')
status, output = commands.getstatusoutput("ils " + SHARED_SPACE)

if status != 0:
    if output.find('command not found') > -1:
        path = os.environ["PATH"]
        if path.find('icommands') < 0:
            path = path + ":" + IRODS_DIR + "/clients/icommands/bin"
            os.putenv('PATH', path)
            status, output = commands.getstatusoutput("ils " + SHARED_SPACE)
if status != 0:
    if output.find('does not exist or user lacks access permission') > -1:
        print "shared space you entered does not exist. "\
"Please, check b2safe.config and rerun the install script"
        exit()
    else: 
        print output
        exit()

for i in range(1, len(us)):
    os.system("ichmod -r own " + us[i] + " " + SHARED_SPACE)

print GREEN + BOLD + 'B2SAFE module installation is' \
            + RED + BOLD + ' ALMOST ' + GREEN + BOLD + 'finished!' + BACK
print BLUE + BOLD + 'Please, complete the following steps ' \
      'to be able to use the module: \n '\
      '- change "#!/usr/bin/env python" in python scripts in ' \
      'modules/B2SAFE/cmd/ to your python installation \n '\
      '- install httplib2, simplejson and pylint: \n '\
      '  httplib2: \n '\
      '    download from http://code.google.com/p/httplib2 \n '\
      '    python setup.py install \n '\
      '  simplejson: \n '\
      '    download from http://pypi.python.org/pypi/simplejson/ \n '\
      '    python setup.py install \n '\
      '  ubuntu: apt-get install python-httplib2 python-simplejson \n '\
      '  ubuntu: apt-get install pylint \n '\
      '- install queuelib library to run logging-mechanism \n '\
      '- test the epic api interaction by running the '\
      '"' + IRODS_DIR + '/modules/B2SAFE/cmd/epicclient.py os '\
      + IRODS_DIR + '/modules/B2SAFE/conf/credentials test"'\
      ' script manually and with "iexecmd epicclient.py" \n '\
      '- test replication by changing and triggering test rules '\
      'in' + IRODS_DIR + '/modules/B2SAFE/rules' + BACK

exit()

