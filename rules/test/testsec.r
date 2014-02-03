#
# used to test microservice msiExecCmd
#

test {		
	
	getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);	
   	msiExecCmd("epicclient.py", "*credStoreType *credStorePath delete *pid", "null", "null", "null", *out2);
}

INPUT *pid="848/57f5d646-8440-11e3-9e75-fa163e4a8cc3"
OUTPUT ruleExecOut