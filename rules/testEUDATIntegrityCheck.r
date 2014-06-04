#
# Test integrity check between 2 collections
#

test {
	EUDATIntegrityCheck(*Path,*replicaPath);
	
	}

INPUT *Path="/COMMUNITY/DATA/Ordner6",*replicaPath="/DATACENTER/Data17/Ordner6"
OUTPUT ruleExecOut

