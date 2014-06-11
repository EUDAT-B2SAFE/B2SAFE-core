#
# Test Do Replication
#
# 1.Test:
# (with msiCollCreate) 
# Source: /DATACENTER2/DATA/xaaaaaaaadv, Destination: /DATACENTER2/DATA/Test/xaaaaaaaadv
# Result: DONE, OK.
#
# 2.Test:
# (without msiCollCreate)
# Source: /DATACENTER2/DATA/xaaaaaaaadv, Destination: /DATACENTER2/DATA/Test2/xaaaaaaaadv
# Result: DONE, OK.
#
test {

	msiSplitPath(*destination, *parent, *child);
	
	# Test with/ without this microservice
    msiCollCreate(*parent, "1", *collCreateStatus);

    #rsync object (make sure to supply "null" if dest resource should be the default one) 
    msiDataObjRsync(*source, "IRODS_TO_IRODS", "null", *destination, *rsyncStatus);

}
INPUT  *source = "/DATACENTER2/DATA/xaaaaaaaadv", *destination = "/DATACENTER2/DATA/Test/xaaaaaaaadv"
OUTPUT ruleExecOut