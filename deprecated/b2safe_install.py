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
    if line.find('IRODS_CONF_DIR') > -1:
        ircod = line.split()
    if line.find('IRODS_SERVER_CONF_DIR') > -1:
        irscod = line.split()
    if line.find('SOURCE_DIR') > -1:
        tr = line.split()
    if line.find('CONF_DIR:') > -1:
        cod = line.split()
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
fr.close()    

IRODS_DIR = ird[1]
IRODS_CONF_DIR = ircod[1]
IRODS_SERVER_CONF_DIR = irscod[1]
SOURCE_DIR = tr[1]
CONF_DIR = cod[1]
DEFAULT_RESOURCE = dr[1]
CRED_STORE_TYPE = cst[1]
CRED_FILE_PATH = cfp[1]
SERVER_ID = si[1]
BASEURI = bu[1]
USERNAME = un[1]
PREFIX = pf[1]
LOG_LEVEL = ll[1]
LOG_DIR = ld[1]

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

def symlink(orign, link, oldlink1):
    """ create symbolic links """
    subprocess.call(["rm", "-f", oldlink1])
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
      'module' + BACK
print BLUE + BOLD + 'CAUTION: ' \
      'If there is a previuos version of the B2SAFE module installed ' \
      'it will be overwritten. \n' + BACK

inp = raw_input(BLUE + BOLD + 'Continue installation (y/n)? :' + BACK).lower()

chk = inpt(inp)

print BLUE + BOLD + 'CAUTION: ' \
            'If you were using a previuos version of the B2SAFE module, \n' \
            '1) your ' + IRODS_CONF_DIR + ' '\
            'may contain symbolic ' \
            'links to B2SAFE rule sets of the previous version. '\
            'They may have (but not must and are not limited to) ' \
            'names like: \n' \
            + IRODS_DIR + '/server/config/reConfigs/eudat.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eurepl.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/catchError.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eucerr.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/local.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/euloc.re \n' \
            '2)your ' + IRODS_DIR + '/server/bin/cmd/ may contain' \
            ' symbolic links to ' \
            'B2SAFE scripts of the previous version. They may have (but not ' \
            'must and are not limited to) names like: \n' \
            + IRODS_DIR + '/server/bin/cmd/authZmanager.py \n' \
            + IRODS_DIR + '/server/bin/cmd/authz.map.json \n' \
            + IRODS_DIR + '/server/bin/cmd/credentials_example \n' \
            + IRODS_DIR + '/server/bin/cmd/credentials \n' \
            + IRODS_DIR + '/server/bin/cmd/epicclient.py \n' \
            + IRODS_DIR + '/server/bin/cmd/log.manager.conf \n' \
            + IRODS_DIR + '/server/bin/cmd/logmanager.py \n' \
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

print '1. copy source conf dir to conf_dir'

try:
    subprocess.check_call(["stat", CONF_DIR])
except subprocess.CalledProcessError:
    print BLUE + BOLD + 'Creating directory ' + CONF_DIR + '..' + BACK
    try:
        subprocess.check_call(["mkdir", CONF_DIR])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: directory ' + CONF_DIR + ' cannot be ' \
          'created. \nPlease, check the path in the b2safe.config ' \
          '(CONF_DIR) \nand access permissions and start over again.' \
          + BACK
        exit()
    else:
        subprocess.call(["mkdir", CONF_DIR])
else:
    print RED + BOLD + 'Directory ' + CONF_DIR + ' exists. \n' + BACK
    inp = raw_input(RED + BOLD + 'Should it be overwritten (y/n)? :' \
          + BACK).lower()
    chk = inpt(inp)

try:
    subprocess.check_call(["stat", SOURCE_DIR])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Directory ' + SOURCE_DIR + ' does not exist.' \
          'Please, check the SOURCE_DIR in 2safe.config. ' \
          'It should point to the place where you have downloaded ' \
          'the git repository' + BACK
    exit()

try:
    subprocess.call(["cp", "-r"] + glob.glob(os.path.join(SOURCE_DIR \
                    + "/conf", '*')) + [CONF_DIR])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: cannot copy ' + SOURCE_DIR + '/conf to ' \
          + CONF_DIR + '\nPlease, check access permissions and start over' \
          ' again.' + BACK
    exit()

print '2. create symbolic links to the eudat rulebase'

symlink(SOURCE_DIR + "/rulebase/eudat.re", \
        IRODS_CONF_DIR + "/eudat.re", \
        IRODS_CONF_DIR + "/eudat.re")

symlink(SOURCE_DIR + "/rulebase/replication.re", \
        IRODS_CONF_DIR + "/eurepl.re", \
        IRODS_CONF_DIR + "/eurepl.re")

symlink(SOURCE_DIR + "/rulebase/pid-service.re", \
        IRODS_CONF_DIR + "/eupids.re", \
        IRODS_CONF_DIR + "/eupids.re")

symlink(SOURCE_DIR + "/rulebase/catchError.re", \
        IRODS_CONF_DIR + "/eucerr.re", \
        IRODS_CONF_DIR + "/eucerr.re")

symlink(SOURCE_DIR + "/rulebase/local.re", \
        IRODS_CONF_DIR + "/euloc.re", \
        IRODS_CONF_DIR + "/euloc.re")
        
print '3. edit <irods>/server/config/server.config and append '\
',eudat,eurepl,eupids,eucerr,euloc'\
',to reRuleSet (make sure to include the comma and no spaces)'

filename = IRODS_SERVER_CONF_DIR + "/server.config"
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
            line1 = line1.replace(",eudat-authZ-filters","")
            line1 = line1.replace("eudat-authZ-filters,","")
            line1 = line1.replace(",authZ","")
            line1 = line1.replace("authZ,","")
            line1 = line1.replace("local","euloc")
            line1 = line1.replace(",integritycheck","")
            line1 = line1.replace("integritycheck,","")
            destination.write(line1)
        elif (line.find('euaf') > -1) or \
(line.find('euint') > -1):
            line1 = line.replace(",euaf","")
            line1 = line1.replace("euaf,","")
            line1 = line1.replace(",euint","")
            line1 = line1.replace("euint,","")
            destination.write(line1)
        else:
            destination.write(line)
    else:
        destination.write(line)
source.close()
destination.close()

print '4. properly configure the default resource in '\
'/etc/<irods>/core.re \n'

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

print '5.1 install python scripts \n     cd <irods> \n     '\
'ln -s <absolute-b2safe-core-source-path>/cmd/* '\
'./server/bin/cmd/ \n     check permissions on the scripts '\
'and make sure they are executable by the irods user \n'\
'         e.g.chmod u+x cmd/* \n'

stat(SOURCE_DIR + "/cmd")

subprocess.call(["chmod", "u+x"] + \
                 glob.glob(os.path.join(SOURCE_DIR, 'cmd', '*')))

subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authZmanager.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authz.map.json"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/authz.map.json~"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/credentials_example"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/credentials"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/epicclient.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/log.manager.conf"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/log.manager.conf~"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/logmanager.py"])
subprocess.call(["rm", "-f", IRODS_DIR + "/server/bin/cmd/statpid.py"])

try:
    subprocess.check_call(["ln", "-s"] + \
    glob.glob(os.path.join(SOURCE_DIR, 'cmd', '*')) + \
    [IRODS_DIR + "/server/bin/cmd/"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: failed to create symbolic link:\n' + \
          IRODS_DIR + '/server/bin/cmd/*\nPlease, check command line output ' \
          'and start over again.' + BACK
    exit()

try:
    subprocess.check_call(["ln", "-s"] + \
    glob.glob(os.path.join(CONF_DIR, '', '*')) + \
    [IRODS_DIR + "/server/bin/cmd/"])
except subprocess.CalledProcessError:
    print RED + BOLD + 'Error: failed to create symbolic link:\n' + \
          IRODS_DIR + '/server/bin/cmd/*\nPlease, check command line output ' \
          'and start over again.' + BACK
    exit()

print "5.2 update the 'getEpicApiParameters' rule in "\
"'/etc/<irods>/euloc.re' \n     "\
"- Configure the credential storage type: 'os': "\
"stored on the local filesystem or 'irods': stored on de irods namespace. "\
"\n     - Set the path to the credentials file \n"\
"     - set the correct serverID to include the fully qualified hostname. "\
"For instance: 'irods://node.domain.com:1247' \n     "\
"- Set the proper values in the credentials file "\
"(see <b2safe-core-source>/conf/credentials_example for an example) "

filename = IRODS_CONF_DIR + "/euloc.re"
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
"cmd/authz.map.json",CONF_DIR+"/authz.map.json")
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf",\
CONF_DIR+"/log.manager.conf")
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/metadataManager.conf"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/metadataManager.conf",\
CONF_DIR+"/metadataManager.conf")
        destination.write(line1)
    elif line.find(\
'"/var/log/irods/messageManager.log"') > -1:
        line1 = line.replace(\
"/var/log/irods/messageManager.log",\
CONF_DIR+"/log/messageManager.log")
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print "- Set the proper values in the credentials "\
"file (see <b2safe-core-source>/conf/credentials_example for an example)"

filename = CONF_DIR + "/credentials_example"
stat(filename)
destination = open(CONF_DIR+"/credentials","w")
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
symlink(CONF_DIR + "/credentials", \
        IRODS_DIR + "/server/bin/cmd/credentials", \
        IRODS_DIR + "/server/bin/cmd/credentials")

print '5.3 update the "getAuthZParameters" rule in '\
'"/etc/<irods>/euloc.re" \n - '\
'Set the proper values in CONF_DIR/authz.map.json'

filename = CONF_DIR + "/authz.map.json"
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
        destination.write('                [ "*.py" ' + ',')
        destination.write(' "*" ]' + '\n')
    elif line.find('"*"') < 0:
        destination.write(line)
source.close()
destination.close()

print '5.4 update the "getLogParameters" rule in '\
'"/etc/<irods>/euloc.re" \n '\
'- Set the proper values in CONF_DIR/log.manager.conf'

try:
    subprocess.check_call(["stat", LOG_DIR])
except subprocess.CalledProcessError:
    print BLUE + BOLD + 'Creating directory ' + LOG_DIR + '..' + BACK
    try:
        subprocess.check_call(["mkdir", LOG_DIR])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: directory ' + LOG_DIR + ' cannot be ' \
          'created. \nPlease, check the path in the b2safe.config ' \
          '(CONF_DIR) \nand access permissions and start over again.' \
          + BACK
        exit()
    else:
        subprocess.call(["mkdir", LOG_DIR])
else:
    print BLUE + BOLD + 'Directory ' + LOG_DIR + ' exists. \n' + BACK

filename = CONF_DIR + "/log.manager.conf"
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

print '5.5 update the "getMetaParameters" rule in '\
'"/etc/<irods>/euloc.re" \n '\
'- Set the proper values in CONF_DIR/metadataManager.conf'

try:
    subprocess.check_call(["stat", LOG_DIR])
except subprocess.CalledProcessError:
    print BLUE + BOLD + 'Creating directory ' + LOG_DIR + '..' + BACK
    try:
        subprocess.check_call(["mkdir", LOG_DIR])
    except subprocess.CalledProcessError:
        print RED + BOLD + 'Error: directory ' + LOG_DIR + ' cannot be ' \
          'created. \nPlease, check the path in the b2safe.config ' \
          '(CONF_DIR) \nand access permissions and start over again.' \
          + BACK
        exit()
    else:
        subprocess.call(["mkdir", LOG_DIR])
else:
    print BLUE + BOLD + 'Directory ' + LOG_DIR + ' exists. \n' + BACK

filename = CONF_DIR + "/metadataManager.conf"
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
    if line.find('log_file') > -1:
        line1 = line.replace("/var/log/irods", LOG_DIR)
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print GREEN + BOLD + 'B2SAFE module installation is' \
            + RED + BOLD + ' ALMOST ' + GREEN + BOLD + 'finished!' + BACK
print BLUE + BOLD + 'Please, complete the following steps ' \
      'to be able to use the module: \n '\
      '- change "#!/usr/bin/env python" in python scripts in ' \
      '<b2safe-core-source>/cmd/ to your python installation \n '\
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
      + BACK

exit()

