#!/usr/bin/python
""" B2SAFE automatic deployment """
import os
import getpass
import commands

# colors for terminal output

RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
BACK = '\033[0m'
BOLD = '\033[1m'

# read and set config values

filename = "./b2safe.config"
fr = open(filename,'r')
lines = fr.readlines()
for line in lines:
    if line.find('IRODS_DIR') > -1:
        ird = line.split()
    if line.find('TRUNK') > -1:
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
TRUNK = tr[1]
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

# y/n exit

def inpt(inp1):
    """ y/n exit """
    for j in range(3):
        if inp1 == 'y':
            break
        if inp1 == 'n':
            exit()
        else:
            inp1 = raw_input(RED + 'Please, respond in (y/n) :' + BACK).lower()
    if inp1 == 'y':
        return True
    else:
        exit()
    return False

# welcome msgs

print GREEN + BOLD + 'Welcome! \n This script will install EUDAT B2SAFE module ' \
      'in the following directory: ' + B2_MOD_DIR + BACK
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
            + IRODS_DIR + '/server/config/reConfigs/euaf.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/eudat-authZ-filters.re\n' \
            + IRODS_DIR + '/server/config/reConfigs/authZ.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/local.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/euloc.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/integritycheck.re \n' \
            + IRODS_DIR + '/server/config/reConfigs/euint.re \n' \
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
            'the installation again.' + BACK

inp = raw_input(BLUE + BOLD + 'Continue installation (y/n)? :' + BACK).lower()

chk = inpt(inp)

print 'copy trunk to modules dir in irods'

os.system("mkdir " + B2_MOD_DIR)
os.system("cp -r " + TRUNK + "/* " + B2_MOD_DIR)

os.system("mkdir " + B2_MOD_DIR + "/microservices/obj")

filename =  B2_MOD_DIR + "/Makefile"
os.rename(filename, filename+"~")
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

os.chdir(IRODS_DIR)
os.system(IRODS_DIR + "/scripts/configure --enable-B2SAFE")

print '1.2. make clean'
os.chdir(IRODS_DIR)
os.system("make clean")

print '1.3. make'
os.system("make")

print '1.4 <irods>/irodsctl restart'

os.system(IRODS_DIR + "/irodsctl restart")

print '2. create symbolic links'\
' to the eudat rulebase'

os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/eudat.re")
os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/eudat-v1.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/eudat.re " + IRODS_DIR + \
"/server/config/reConfigs/eudat.re")

os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/replication.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/eurepl.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/replication.re " + \
IRODS_DIR + "/server/config/reConfigs/eurepl.re")

os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/pid-service.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/eupids.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/pid-service.re " + \
IRODS_DIR + "/server/config/reConfigs/eupids.re")

os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/catchError.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/eucerr.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/catchError.re " + \
IRODS_DIR + "/server/config/reConfigs/eucerr.re")

os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/euaf.re")
os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/eudat-authZ-filters.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/authZ.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/authZ.re " + \
IRODS_DIR + "/server/config/reConfigs/euaf.re")

os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/local.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/euloc.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/local.re " + \
IRODS_DIR + "/server/config/reConfigs/euloc.re")

os.system("rm -f " + IRODS_DIR + \
"/server/config/reConfigs/integritycheck.re")
os.system("rm -f " + IRODS_DIR + "/server/config/reConfigs/euint.re")
os.system("ln -s " + B2_MOD_DIR + "/rulebase/integritycheck.re " + \
IRODS_DIR + "/server/config/reConfigs/euint.re")


print '3. edit <irods>/server/config/server.config and append '\
',eudat,replication,pid-service,catchError,eudat-authZ-filters'\
',local to reRuleSet (make sure to include the comma and no spaces)'


filename = IRODS_DIR + "/server/config/server.config"
os.rename(filename, filename+"~")
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('reRuleSet') > -1:
        if (line.find('eudat') < 0) and \
(line.find('replication') < 0):
            destination.write(line.strip("\n") + \
",eudat,eurepl,eupids,eucerr,euaf,euloc,euint" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') < 0) and (line.find('eurepl') < 0):
            destination.write(line.strip("\n") + \
",eurepl,eupids,eucerr,euaf,euloc,euint" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') > -1):
            line1 = line.replace("replication","eurepl")
            line1 = line1.replace("pid-service","eupids")
            line1 = line1.replace("catchError","eucerr")
            line1 = line1.replace("eudat-authZ-filters","euaf")
            line1 = line1.replace("authZ","euaf")
            line1 = line1.replace("eudat-authZ-filters","euaf")
            line1 = line1.replace("local","euloc")
            line1 = line1.replace("integritycheck","euint")
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

def check(strr, fname):
    """ check if string is in file """
    datafile = file(fname) 
    for lin in datafile:
        if strr in lin: 
            return True
    return False

filename = IRODS_DIR + "/server/config/reConfigs/core.re"
if not check("\*.pid.create", filename):
    print filename
    os.rename(filename, filename+"~")
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
    os.rename(filename, filename+"~")
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

os.system("chmod u+x " + B2_MOD_DIR + "/cmd/*")

os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/authZ.manager.py")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/authz.map.json")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/authz.map.json~")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/credentials_example")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/credentials")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/epicclient.py")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/epicclient21.py")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/log.manager.conf")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/log.manager.conf~")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/log.manager.py")
os.system("rm -f " + IRODS_DIR + "/server/bin/cmd/statpid.py")

os.system("ln -s " + B2_MOD_DIR + "/cmd/* " + IRODS_DIR + "/server/bin/cmd/")
os.system("ln -s " + B2_MOD_DIR + "/conf/* " + IRODS_DIR + "/server/bin/cmd/")

print "6.2 update the 'getEpicApiParameters' rule in "\
"'./server/config/reConfigs/local.re' \n     "\
"- Configure the credential storage type: 'os': "\
"stored on the local filesystem or 'irods': stored on de irods namespace. "\
"\n     - Set the path to the credentials file \n"\
"     - set the correct serverID to include the fully qualified hostname. "\
"For instance: 'irods://node.domain.com:1247' \n     "\
"- Set the proper values in the credentials file "\
"(see ./cmd/credentials_example for an example) "

filename = B2_MOD_DIR + "/rulebase/local.re"
os.rename(filename, filename+"~")
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
"file (see ./cmd/credentials_example for an example)"

filename = B2_MOD_DIR + "/conf/credentials_example"
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
        print BLUE + "Please, enter your password for your prefix " \
              + PREFIX + ":" + BACK
        password = getpass.getpass()
        line1 = line.replace("YYYYYYYY", password)
        destination.write(line1)
    else:
        destination.write(line)
source.close()
destination.close()

print '6.3 update the "getAuthZParameters" rule in '\
'"./server/config/reConfigs/local.re" \n - '\
'Set the proper values in modules/B2SAFE/cmd/authz.map.json'

filename = B2_MOD_DIR + "/conf/authz.map.json"
os.rename(filename, filename+"~")
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
'"./server/config/reConfigs/local.re" \n '\
'- Set the proper values in modules/B2SAFE/cmd/log.manager.conf'

filename = B2_MOD_DIR + "/conf/log.manager.conf"

os.rename(filename, filename+"~")
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
print GREEN + BOLD + 'Please, complete the following steps ' \
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
      '- test the epic api interaction by running the '\
      '"./cmd/epicclient.py test" script manually and with '\
      '"iexecmd epicclient.py" \n '\
      '- test the replication by changing and triggering "replicate.r" '\
      'rule in <irods>/modules/B2SAFE/rules' + BACK


exit()

