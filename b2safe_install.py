#!/usr/bin/python
""" B2SAFE automatic deployment """
import os
import getpass
import commands

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

irods_dir = ird[1]
trunk = tr[1]
b2_mod_dir = bmd[1]
default_resource = dr[1]
cred_store_type = cst[1]
cred_file_path = cfp[1]
server_id = si[1]
baseuri = bu[1]
username = un[1]
prefix = pf[1]
log_level = ll[1]
log_dir = ld[1]
shared_space = hs[1]

print 'copy trunk to modules dir in irods'

os.system("mkdir " + b2_mod_dir)
os.system("cp -r " + trunk + "/* " + b2_mod_dir)

print '1.1. <irods>/scripts/configure --enable-B2SAFE \n'\
'If a previous version of the module is present, \n'\
'disable it before to install the new one \n'\
'(if the directory name is the same, change it): \n'\
'<irods>/scripts/configure --disable-OLD_MODULE --enable-B2SAFE'

os.chdir(irods_dir)
os.system(irods_dir + "/scripts/configure --enable-B2SAFE")

print '1.2. make clean'
os.chdir(irods_dir)
os.system("make clean")

print '1.3. make'
os.system("make")

print '1.4 <irods>/irodsctl restart'

os.system(irods_dir + "/irodsctl restart")

print '2. create symbolic links'\
' to the eudat rulebase'

os.system("rm -f " + irods_dir + "/server/config/reConfigs/eudat.re")
os.system("rm -f " + irods_dir + \
"/server/config/reConfigs/eudat-v1.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/eudat.re " + irods_dir + \
"/server/config/reConfigs/eudat.re")

os.system("rm -f " + irods_dir + \
"/server/config/reConfigs/replication.re")
os.system("rm -f " + irods_dir + "/server/config/reConfigs/eurepl.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/replication.re " + \
irods_dir + "/server/config/reConfigs/eurepl.re")

os.system("rm -f " + irods_dir + \
"/server/config/reConfigs/pid-service.re")
os.system("rm -f " + irods_dir + "/server/config/reConfigs/eupids.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/pid-service.re " + \
irods_dir + "/server/config/reConfigs/eupids.re")

os.system("rm -f " + irods_dir + \
"/server/config/reConfigs/catchError.re")
os.system("rm -f " + irods_dir + "/server/config/reConfigs/eucerr.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/catchError.re " + \
irods_dir + "/server/config/reConfigs/eucerr.re")

os.system("rm -f " + irods_dir + "/server/config/reConfigs/euaf.re")
#os.system("rm -f " + irods_dir + \
#"/server/config/reConfigs/eudat-authZ-filters.re")
os.system("rm -f " + irods_dir + "/server/config/reConfigs/authZ.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/authZ.re " + \
irods_dir + "/server/config/reConfigs/euaf.re")

os.system("rm -f " + irods_dir + "/server/config/reConfigs/local.re")
os.system("rm -f " + irods_dir + "/server/config/reConfigs/euloc.re")
os.system("ln -s " + b2_mod_dir + "/rulebase/local.re " + \
irods_dir + "/server/config/reConfigs/euloc.re")

#os.system("rm -f " + irods_dir + \
#"/server/config/reConfigs/integritycheck.re")
#os.system("rm -f " + irods_dir + "/server/config/reConfigs/euint.re")
#os.system("ln -s " + b2_mod_dir + "/rulebase/integritycheck.re " + \
#irods_dir + "/server/config/reConfigs/euint.re")


print '3. edit <irods>/server/config/server.config and append '\
',eudat,replication,pid-service,catchError,authZ'\
',local to reRuleSet (make sure to include the comma and no spaces)'


filename = irods_dir + "/server/config/server.config"
os.rename(filename, filename+"~")
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('reRuleSet') > -1:
        if (line.find('eudat') < 0) and \
(line.find('replication') < 0):
            destination.write(line.strip("\n") + \
",eudat,eurepl,eupids,eucerr,euaf,euloc" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') < 0) and (line.find('eurepl') < 0):
            destination.write(line.strip("\n") + \
",eurepl,eupids,eucerr,euaf,euloc" + "\n")
        elif (line.find('eudat') > -1) and \
(line.find('replication') > -1):
            line1 = line.replace("replication","eurepl")
            line1 = line1.replace("pid-service","eupids")
            line1 = line1.replace("catchError","eucerr")
#            line1 = line1.replace("eudat-authZ-filters","euaf")
            line1 = line1.replace("authZ","euaf")
#            line1 = line1.replace("eudat-authZ-filters","euaf")
            line1 = line1.replace("local","euloc")
#            line1 = line1.replace("integritycheck","euint")
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
    for li in datafile:
        if strr in li: 
            return True
    return False

filename = irods_dir + "/server/config/reConfigs/core.re"
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
 + default_resource + '","null"); }',filename) \
and default_resource != 'demoResc':
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
'{msiSetDefaultResc("' + default_resource + '","null"); }' + '\n')
            destination.write('acSetRescSchemeForRepl '\
'{msiSetDefaultResc("' + default_resource + '","null"); }' + '\n')
        else:
            destination.write(line)
    source.close()
    destination.close()

print '6.1 install python scripts \n     cd <irods> \n     '\
'ln -s <absolute-irods-path>/modules/B2SAFE/cmd/* '\
'./server/bin/cmd/ \n     check permissions on the scripts '\
'and make sure they are executable by the irods user \n'\
'         e.g.chmod u+x cmd/* \n'

os.system("chmod u+x " + b2_mod_dir + "/cmd/*")

os.system("rm -f " + irods_dir + "/server/bin/cmd/authZ.manager.py")
os.system("rm -f " + irods_dir + "/server/bin/cmd/authz.map.json")
os.system("rm -f " + irods_dir + "/server/bin/cmd/authz.map.json~")
os.system("rm -f " + irods_dir + "/server/bin/cmd/credentials_example")
os.system("rm -f " + irods_dir + "/server/bin/cmd/credentials")
os.system("rm -f " + irods_dir + "/server/bin/cmd/epicclient.py")
os.system("rm -f " + irods_dir + "/server/bin/cmd/epicclient21.py")
os.system("rm -f " + irods_dir + "/server/bin/cmd/log.manager.conf")
os.system("rm -f " + irods_dir + "/server/bin/cmd/log.manager.conf~")
os.system("rm -f " + irods_dir + "/server/bin/cmd/log.manager.py")
os.system("rm -f " + irods_dir + "/server/bin/cmd/statpid.py")

os.system("ln -s " + b2_mod_dir + "/cmd/* " + irods_dir + "/server/bin/cmd/")

print "6.2 update the 'getEpicApiParameters' rule in "\
"'./server/config/reConfigs/local.re' \n     "\
"- Configure the credential storage type: 'os': "\
"stored on the local filesystem or 'irods': stored on de irods namespace. "\
"\n     - Set the path to the credentials file \n"\
"     - set the correct serverID to include the fully qualified hostname. "\
"For instance: 'irods://node.domain.com:1247' \n     "\
"- Set the proper values in the credentials file "\
"(see ./cmd/credentials_example for an example) "

filename = b2_mod_dir + "/rulebase/local.re"
os.rename(filename, filename+"~")
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('"os"') > -1:
        line1 = line.replace("os", cred_store_type)
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/credentials_test"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/credentials_test",cred_file_path)
        destination.write(line1)
    elif line.find('"irods://<hostnameWithFullDomain>:1247"') > -1:
        line1 = line.replace("irods://<hostnameWithFullDomain>:1247", server_id)
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/authz.map.json"') > -1:
        line1 = line.replace("/srv/irods/current/modules/B2SAFE/"\
"cmd/authz.map.json",b2_mod_dir+"/cmd/authz.map.json")
        destination.write(line1)
    elif line.find(\
'"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf"') > -1:
        line1 = line.replace(\
"/srv/irods/current/modules/B2SAFE/cmd/log.manager.conf",\
b2_mod_dir+"/cmd/log.manager.conf")
        destination.write(line1) 	
    else:
        destination.write(line)
source.close()
destination.close()

print "- Set the proper values in the credentials "\
"file (see ./cmd/credentials_example for an example)"

filename = b2_mod_dir + "/cmd/credentials_example"
destination = open(b2_mod_dir+"/cmd/credentials","w")
source = open(filename, "r")
for line in source:
    if line.find('"baseuri"') > -1:
        line1 = line.replace("https://epic.sara.nl/v2_test/handles/", baseuri)
        destination.write(line1)
    elif line.find('"username"') > -1:
        line1 = line.replace("XXX", username)
        destination.write(line1)
    elif line.find('"prefix"') > -1:
        line1 = line.replace("ZZZ", prefix)
        destination.write(line1)
    elif line.find('"password"') > -1:
        print "please, enter your password for your prefix:"
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

filename = b2_mod_dir + "/cmd/authz.map.json"
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
        destination.write('                [ "'+b2_mod_dir+'/cmd/*" ]' + '\n')
    elif line.find('"*"') < 0:
        destination.write(line)
source.close()
destination.close()

print '6.4 update the "getLogParameters" rule in '\
'"./server/config/reConfigs/local.re" \n '\
'- Set the proper values in modules/B2SAFE/cmd/log.manager.conf'

filename = b2_mod_dir + "/cmd/log.manager.conf"

os.rename(filename, filename+"~")
destination = open(filename, "w")
source = open(filename+"~", "r")
for line in source:
    if line.find('"log_level"') > -1:
        line1 = line.replace("DEBUG", log_level)
        destination.write(line1)
    elif line.find('"log_dir"') > -1:
        line1 = line.replace("/srv/irods/current/modules/B2SAFE/log", log_dir)
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
    path = path + ":" + irods_dir + "/clients/icommands/bin"
    os.putenv('PATH', path)
    os.system('bash')
status, output = commands.getstatusoutput("ils " + shared_space)

if status != 0:
    if output.find('command not found') > -1:
        path = os.environ["PATH"]
        if path.find('icommands') < 0:
            path = path + ":" + irods_dir + "/clients/icommands/bin"
            os.putenv('PATH', path)
            status, output = commands.getstatusoutput("ils " + shared_space)
if status != 0:
    if output.find('does not exist or user lacks access permission') > -1:
        print "shared space you entered does not exist. "\
"Please, check b2safe.config and rerun the install script"
        exit()
    else: 
        print output
        exit()

for i in range(1, len(us)):
    os.system("ichmod -r own " + us[i] + " " + shared_space)




exit()


